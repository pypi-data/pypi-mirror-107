# -*- coding: utf-8 -*-

import scipy.io.wavfile as wf
import numpy as np


def get_sound(in_file, sampling_rate=441, cutoff=None, silence=None, out=None):
    """
    A function for sound detection. Can write filtered audio files, too.

    Parameters
    ----------
    in_file: string
        Path to the target sound file.
    sampling_rate: int, optional
        Sample rate for evaluation.
        A smaller rate improves speed and gets less detailed.
    cutoff: float, optional
        Silence threshold in dB. Has to be negative! If None the function will
        return the maximum amplitude value.
    silence: int, optional
        Minimal silence duration in ms. Smaller gaps between sound
        occurences will be removed.
    out: string, optional
        Path to filtered sound file. If this parameter is set,
        the function will write a filtered sound file to the path.

    Returns
    -------
    sound: list
        a list containing whether sound was detected (1) or not (0) at time t.
        When cutoff is None, sound and vals return the same data.
    vals: list
        a list containing energy values

    """
    in_samplerate, in_data = wf.read(in_file)
    in_data = in_data / np.iinfo(in_data.dtype).max
    sample_count = in_samplerate // sampling_rate
    if silence is not None:
        silence_ts = sampling_rate * silence/1000.0
    nframes = in_data.shape[0]
    out_file = np.zeros(in_data.shape)
    sound = []
    vals = []
    current = 0
    while nframes > 0:
        nsample = min([nframes, sample_count])
        data = in_data[current:current+nsample]
        # $ E = \frac 1 N \sum_{i=1}^N s_i $
        val = np.max(data**2)
        val = np.log10(val) * 10
        if cutoff is None:
            res = val
            out_file[current:current+nsample] = data
        elif val < cutoff:
            res = 0
        else:
            res = 1
            out_file[current:current+nsample] = data
        sound.append(res)
        vals.append(val)
        nframes -= nsample
        current += nsample
    if out is not None:
        wf.write(out, in_samplerate, out_file)
    if silence is not None and cutoff is not None:
        last_idx = 0
        for idx, i in enumerate(sound):
            if i == 1:
                if idx - last_idx < silence_ts:
                    sound[last_idx:idx] = [1]*(idx - last_idx)
                last_idx = idx
    return sound, vals


# https://github.com/marsbroshok/VAD-python
class VoiceActivityDetector():
    """ Use signal energy to detect voice activity in wav file """

    def __init__(self, wave_input_filename=None, window=20):
        if wave_input_filename is not None:
            self.load_wav(wave_input_filename)._convert_to_mono()
        self.sample_window = window
        self.sample_overlap = window * 0.5
        self.speech_window = 0.5 #half a second
        self.speech_energy_threshold = 0.6 #60% of energy in voice band
        self.speech_start_band = 300
        self.speech_end_band = 3000

    def load_wav(self, wave_file):
        self.rate, self.data = wf.read(wave_file)
        self.channels = len(self.data.shape)
        self.filename = wave_file
        return self

    def _convert_to_mono(self):
        if self.channels == 2:
            self.data = np.mean(self.data, axis=1, dtype=self.data.dtype)
            self.channels = 1
        return self

    def _calculate_frequencies(self, audio_data):
        data_freq = np.fft.fftfreq(len(audio_data),1.0/self.rate)
        data_freq = data_freq[1:]
        return data_freq

    def _calculate_amplitude(self, audio_data):
        data_ampl = np.abs(np.fft.fft(audio_data))
        data_ampl = data_ampl[1:]
        return data_ampl

    def _calculate_energy(self, data):
        data_amplitude = self._calculate_amplitude(data)
        data_energy = data_amplitude ** 2
        return data_energy

    def _znormalize_energy(self, data_energy):
        energy_mean = np.mean(data_energy)
        energy_std = np.std(data_energy)
        energy_znorm = (data_energy - energy_mean) / energy_std
        return energy_znorm

    def _connect_energy_with_frequencies(self, data_freq, data_energy):
        energy_freq = {}
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq

    def _calculate_normalized_energy(self, data):
        data_freq = self._calculate_frequencies(data)
        data_energy = self._calculate_energy(data)
        #data_energy = self._znormalize_energy(data_energy) #znorm brings worse results
        energy_freq = self._connect_energy_with_frequencies(data_freq, data_energy)
        return energy_freq

    def _sum_energy_in_band(self,energy_frequencies, start_band, end_band):
        sum_energy = 0
        for f in energy_frequencies.keys():
            if start_band<f<end_band:
                sum_energy += energy_frequencies[f]
        return sum_energy

    def _median_filter (self, x, k):
        assert k % 2 == 1, "Median filter length must be odd."
        assert x.ndim == 1, "Input must be one-dimensional."
        k2 = (k - 1) // 2
        y = np.zeros ((len (x), k), dtype=x.dtype)
        y[:,k2] = x
        for i in range (k2):
            j = k2 - i
            y[j:,i] = x[:-j]
            y[:j,i] = x[0]
            y[:-j,-(i+1)] = x[j:]
            y[-j:,-(i+1)] = x[-1]
        return np.median (y, axis=1)

    def _smooth_speech_detection(self, detected_windows):
        median_window=int(self.speech_window/self.sample_window)
        if median_window%2==0: median_window=median_window-1
        median_energy = self._median_filter(detected_windows[:,1], median_window)
        return median_energy

    def convert_windows_to_readible_labels(self, detected_windows):
        """ Takes as input array of window numbers and speech flags from speech
        detection and convert speech flags to time intervals of speech.
        Output is array of dictionaries with speech intervals.
        """
        speech_time = []
        is_speech = 0
        for window in detected_windows:
            if (window[1]==1.0 and is_speech==0):
                is_speech = 1
                speech_label = {}
                speech_time_start = window[0] / self.rate
                speech_label['speech_begin'] = speech_time_start
                print(window[0], speech_time_start)
                #speech_time.append(speech_label)
            if (window[1]==0.0 and is_speech==1):
                is_speech = 0
                speech_time_end = window[0] / self.rate
                speech_label['speech_end'] = speech_time_end
                speech_time.append(speech_label)
                print(window[0], speech_time_end)
        return speech_time

    def detect_speech(self):
        """ Detects speech regions based on ratio between speech band energy
        and total energy.
        Output is array of window numbers and speech flags (1 - speech, 0 - nonspeech).
        """

        detected_windows = np.array([])
        sample_window = int(self.rate * self.sample_window)
        sample_overlap = int(self.rate * self.sample_overlap)
        data = self.data
        sample_start = 0
        start_band = self.speech_start_band
        end_band = self.speech_end_band
        while (sample_start < (len(data) - sample_window)):
            sample_end = sample_start + sample_window
            if sample_end>=len(data): sample_end = len(data)-1
            data_window = data[sample_start:sample_end]
            energy_freq = self._calculate_normalized_energy(data_window)
            sum_voice_energy = self._sum_energy_in_band(energy_freq, start_band, end_band)
            sum_full_energy = sum(energy_freq.values())
            speech_ratio = sum_voice_energy/sum_full_energy
            # Hipothesis is that when there is a speech sequence we have ratio of energies more than Threshold
            speech_ratio = speech_ratio>self.speech_energy_threshold
            detected_windows = np.append(detected_windows,[sample_start, speech_ratio])
            sample_start += sample_overlap
        detected_windows = detected_windows.reshape(len(detected_windows)/2,2)
        detected_windows[:,1] = self._smooth_speech_detection(detected_windows)
        return detected_windows
