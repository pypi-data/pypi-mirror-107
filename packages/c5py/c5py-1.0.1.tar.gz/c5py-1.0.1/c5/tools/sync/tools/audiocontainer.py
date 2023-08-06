import numpy as np
from os import mkdir
from os.path import split, splitext
import subprocess
import wave
from scipy import signal
import struct
import getopt
import sys
import time
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AudioContainer:
    def __init__(self, filename, stepsize=120):
        self.__sample = None
        self.__filename = filename
        self.__tempfile = ".tmp_audio/" + splitext(split(filename)[1])[0] + ".wav"
        self.__maxima = []
        self.energy = None
        self.kernel = None
        self.filter = None
        self.__stepsize = stepsize
        self.__frames_to_read = 0
        self.__compression = 0
        self.kernelsize = 0
        self.__storagesize = 0
        self.__synctimes = [[0, 0]]
        self.data = None
        self.used_sync = 0

    @staticmethod
    def prepare():
        try:
            mkdir(".tmp_audio")
        except OSError as e:
            logger.warn(e)

    def init(self, cut_factor=1):
        try:
            call = ["ffmpeg", "-i", self.__filename, "-ac", "1", "-ar", "16000", "-y", self.__tempfile]
            logger.info((' '.join(call)))
            subprocess.check_call(call)
        except Exception as e:
            logger.error("Could not create audio tempfile: %s", e)
            return
        self.__sample = wave.open(self.__tempfile, "r")
        self.kernel = AudioContainer.kernel_func(3, 54, 540)
        self.__compression = self.get_sample_rate() // 441
        self.kernelsize = self.kernel.size * self.__compression
        self.__stepsize = self.__stepsize * self.get_sample_rate()
        self.__stepsize = min(self.__stepsize, (self.get_sample_count() - self.kernelsize))
        self.__storagesize = self.__stepsize + self.kernelsize
        self.set_bandpass(2870, 50)

        logger.debug("kernelsize: %i", self.kernelsize)
        logger.debug("stepsize: %i", self.__stepsize)
        logger.debug("storesize: %i", self.__storagesize)
        logger.debug("compression: %i", self.__compression)
        logger.debug("bins: %i", (self.__storagesize // self.__compression))

        self.data = np.zeros(self.__storagesize, np.dtype('h'))
        if self.get_sample_count() > self.__storagesize*cut_factor:
            self.__frames_to_read = self.get_sample_count() // cut_factor
        tmp = self.__sample.readframes(self.__storagesize)
        self.data = struct.unpack_from("%dh" % self.__storagesize, tmp)
        self.__frames_to_read -= self.__storagesize
        del tmp

    def set_bandpass(self, frequency, band):
        nyquist = self.get_sample_rate() / 2.0
        # normalized frequency
        freq = frequency / nyquist
        # normalized band
        ba = band / nyquist
        # passband
        wp = [freq - ba, freq + ba]
        # stopband;
        ws = [np.max([0, wp[0] - 0.1]), np.min([wp[1] + 0.1, 1])]
        self.filter = signal.iirdesign(wp, ws, gstop=60, gpass=1)

    def load_next(self):
        if self.__frames_to_read < self.__stepsize:
            return False
        self.data[0:self.kernelsize] = self.data[self.data.size-self.kernelsize:]
        bin = self.__sample.readframes(self.__stepsize)
        self.data[self.kernelsize:] = struct.unpack_from("%dh" % self.__stepsize, bin)
        del bin
        self.__frames_to_read -= self.__stepsize
        logger.debug("%i frames to read", self.__frames_to_read)
        return True

    def close(self):
        self.__sample.close()

    def get_sample_count(self):
        return self.__sample.getnframes()

    def get_sample_rate(self):
        return self.__sample.getframerate()

    def get_audio_name(self):
        return self.__tempfile

    def calc_energy(self, steps=1, cutoff=1500):
        self.energy = np.zeros(self.__storagesize // steps, np.float64)
        for i in range(0, self.__storagesize // steps):
            ran = self.data[i*steps:(i+1)*steps]
            val = np.sum(np.abs(ran))
            self.energy[i] = min(cutoff, val)

    @staticmethod
    def kernel_func(os_count, width, distance, negative=True):
        generated = np.zeros((os_count-1) * distance + width)
        window = signal.triang(width)
        nwindow = signal.triang(7*width)
        for i in range(os_count):
            spot = i * distance
            generated[spot:spot+width] = window
            if negative is True and (i < os_count - 1):
                spot += int(0.5 * distance)
                generated[spot-3*width:spot+4*width] = -nwindow
        return generated

    def detect_signal(self):
        self.detection_step()
        while self.load_next() is True:
            self.detection_step()
        self.__synctimes = []
        for idx, val in enumerate(self.__maxima):
            key = (val[0] * self.__compression + idx * self.__stepsize) / float(self.get_sample_rate())
            val = val[1]
            self.__synctimes.append((key, val))
        self.__synctimes = sorted(self.__synctimes, key=lambda x: x[1], reverse=True)
        logger.info("Possible sync event at: %s", str(self.__synctimes))
        logger.debug("Correlation peaks at: %s", str(self.__maxima))
        # set the sync event with the highest confidence
        self.used_sync = self.__synctimes[0][0]

    def detection_step(self):
        self.data = signal.lfilter(self.filter[0], self.filter[1], self.data)
        self.calc_energy(self.__compression)
        res = signal.convolve(self.energy, self.kernel)
        idx = np.argmax(res)
        self.__maxima.append([(idx-self.kernel.size), res[idx]])

    def get_sync_times(self):
        return list(np.array(self.__synctimes)[:, 0])

    def set_used_sync(self, sync_time):
        self.used_sync = sync_time

    def create_sound_file(self, offset):
        try:
            logger.info("Create samples for: %s", str(self.__synctimes))
            subprocess.check_call(["ffmpeg", "-i", self.__filename, "-y", self.__tempfile])
            time.sleep(2)
            if offset > self.used_sync:
                cmd = ["sox", self.__tempfile, ".tmp_audio/long.wav", "pad", str((offset-self.used_sync))]
                logger.info(' '.join(cmd))
                subprocess.check_call(cmd)
                cmd = ["mv", ".tmp_audio/long.wav", self.__tempfile]
                logger.info(' '.join(cmd))
                subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error("Could not create audio tempfile: %s", e)


def extract_audio_sample(filename, offset, duration, destination):
    cmd = ["ffmpeg", "-i", filename, "-ss", str(offset-(duration/2.0)), "-t", str(duration),
           "-acodec", "copy", "-vn", "-y", destination]
    logger.info(' '.join(cmd))
    subprocess.call(cmd)


def usage():
    print("have to write usage some day")
    sys.exit(1)


def main(argv):
    import sys

    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "filename="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--filename"):
            filename = arg
    try:
        filename
    except NameError:
        print("you have to pass the wav file path")
        usage()
        sys.exit(1)

    a1 = AudioContainer(filename)
    AudioContainer.prepare()
    a1.init(cut_factor=2)
    a1.detect_signal()
    print(a1.get_sync_times()[0])

if __name__ == "__main__":
    main(sys.argv[1:])
