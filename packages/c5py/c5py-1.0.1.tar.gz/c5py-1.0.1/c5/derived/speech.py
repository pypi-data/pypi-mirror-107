""" Functions related to speech activity analysis. """

import subprocess
import numpy as np
from numpy.core.records import fromarrays
from scipy.signal import argrelextrema
import os.path
import tempfile
import logging
import c5.audio
import c5.data
import collections
import sys

from c5.config import ConfigLoader, arbc, TRIAL_IDS

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

SPEECH_DT = np.dtype({'names': ['timestamp', 'speech1', 'speech2'],
                     'formats': ['u8', 'i4', 'i4']})


INTERVAL = 20
RATE = 1000 // INTERVAL  # 50Hz


class TempWavContext:

    def __init__(self, wav_file, compression):
        self.wav_file = wav_file
        self.sox_params = ['compand', '0.2,1', '-35,-19,-21,-7', '-1', '-35', '0.2'] if compression else []

    def __enter__(self):
        self.left_fd, self.left_path = tempfile.mkstemp('.wav', prefix='left_')
        self.right_fd, self.right_path = tempfile.mkstemp('.wav', prefix='right_')
        cmd_remix_left = ['sox', self.wav_file, self.left_path] + self.sox_params + ['remix', '1']
        cmd_remix_right = ['sox', self.wav_file, self.right_path] + self.sox_params + ['remix', '2']
        logger.debug('Calling: %s', ' '.join(cmd_remix_left))
        subprocess.call(cmd_remix_left)
        logger.debug('Calling: %s', ' '.join(cmd_remix_right))
        subprocess.call(cmd_remix_right)
        return self.left_path, self.right_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.close(self.left_fd)
        os.close(self.right_fd)
        os.remove(self.left_path)
        os.remove(self.right_path)
        if exc_val is not None:
            logging.warn("Error during processing WAV file: %s", exc_val)
        return True


def use_voice_activity_detector(wav_file, start, compression, **kwargs):
    if os.path.exists(wav_file) is False:
        logger.warning("No soundfile %s found", wav_file)
        return None
    # split stereo channels
    with TempWavContext(wav_file, compression) as (left_path, right_path):
        detector = c5.audio.VoiceActivityDetector(left_path)
        result_left = detector.detect_speech()
        right_sound = c5.audio.VoiceActivityDetector(right_path).detect_speech()[:, 1]
        timestamps = result_left[:, 0] / (detector.rate / 1000.0) + start
        left_sound = result_left[:, 1]
        data = np.column_stack((timestamps, left_sound, right_sound))
        data = fromarrays(data.transpose(), dtype=SPEECH_DT)
        slots = c5.data.create_slots(data, timestamps[0], timestamps[-1]).max()
        slots['delta'] = slots.index.asi8 // 10**6 - slots.timestamp
        slots.drop('timestamp', axis=1, inplace=True)
        slots.index = slots.index.asi8 // 10**6
    return slots


def extract_speech_activity(wav_file, start, sampling_rate=50, compression=True):
    """
    Load a wav sound file and resamples it into a numpy array with a constant sampling rate.

    Parameters
    ----------
    wav_file : str
        Path to a wav file
    start : int
        Timestamp of the recording's start.
    sampling_rate: int, optional
        Sampling rate of the returned array.

    Returns
    -------
    numpy.array or None
        Indexed array of the speech activity or None if wav_file does not exists or wav file is not processable.
    """

    if os.path.exists(wav_file) is False:
        logger.warn("No soundfile %s found", wav_file)
        return None
    with TempWavContext(wav_file, compression) as (left_path, right_path):
        # extract speech activity; ignoring energy values
        # default sampling rate of get_sound is 441 hz which is a decent trade off between accuracy and speed
        left_sound, _ = c5.audio.get_sound(left_path, cutoff=None)
        right_sound, _ = c5.audio.get_sound(right_path, cutoff=None)

        stop = int(start + len(left_sound) / 0.441)
        timestamps = np.arange(start=start, stop=stop, step=1 / 0.441)

        # in rare cases of rounding errors timestamps can be one element too long
        if timestamps.shape[0] - 1 == len(left_sound):
            timestamps = timestamps[:-1]
        data = np.column_stack((timestamps, left_sound, right_sound))
        data = fromarrays(data.transpose(), dtype=SPEECH_DT)
        slots = c5.data.create_slots(data, frame=1000 // sampling_rate).max()
    return slots


def generate_speech_activity(method='extract_speech_activity', compression=True):
    method = getattr(sys.modules[__name__], method)
    db = {}
    for trial in TRIAL_IDS:
        logger.info("Processing data for trial %d", trial)
        con = ConfigLoader(trial)
        start = con.get("mic.start")
        slots = method(wav_file=arbc.stage1.trial(trial).mic_wav(), start=start, compression=compression)
        if slots is not None:
            db[trial] = slots
        else:
            logger.error("Error. No valid data for trial %d", trial)
    return db


def erode_speech_activity(db, thresh=1000, silence=None):
    """
    Load a previously eroded speech activity array or if it does not exist, erode the data in the passed db instead.

    Parameters
    ----------
    db : dict(numpy.array), optional
       A dictionary of speech activity arrays in the format returned by load_speech_activity.
    thresh : int, optional
        Maximum duration in ms of signal gaps which will be removed by erosion.
    silence : int or tuple, optional
        Silence threshold in dB. A sample below this value will be considered silence.

    Returns
    -------
    dict(numpy.array)
        A dictionary of eroded speech activity with trial ids as keys and additional 'meta' information.
    """
    binary = _db_to_binary(db, silence)
    ero = {}
    for key in db:
        ero[key] = erode(binary[key], thresh)
        ero[key] = erode(ero[key], thresh, 0)
    return ero


def _db_to_binary(db, thresh=None):
    res = {}
    for key in db:
        res[key] = db[key].copy()
        if isinstance(thresh, collections.Iterable):
            # negative values are used for db thresholds...
            if thresh[0] < 0:
                spe1 = thresh[0]
                spe2 = thresh[1]
            # positive for percentile values
            else:
                spe1, _ = _percentile_detection(db[key]['speech1'], thresh)
                spe2, _ = _percentile_detection(db[key]['speech2'], thresh)
        else:
            if thresh is None:
                spe1, _ = _range_detection(db[key]['speech1'])
                spe2, _ = _range_detection(db[key]['speech2'])
            else:
                spe1 = spe2 = thresh

        res[key]['speech1'] = (db[key]['speech1'] > spe1).astype(int)
        res[key]['speech2'] = (db[key]['speech2'] > spe2).astype(int)
    return res


def _percentile_detection(data, thresh):
        sil = min(-20, np.percentile(data, thresh[0]))
        spe = min(-5, np.percentile(data[data > sil], thresh[1]))
        return spe, sil


def _range_detection(data, ratio=0.6):
    order = 20
    hist, bins = np.histogram(data, np.arange(-60, 1, 1))
    extrema = argrelextrema(hist, np.greater, order=order)[0]
    while len(extrema) == 0:
        order -= 1
        extrema = argrelextrema(hist, np.greater, order=order)[0]
    sil = bins[extrema[0]]
    spe = sil - sil * ratio
    return spe, sil


def erode(data, thresh, signal=1, columns=['speech1', 'speech2']):
    """
    Erode speech signal data.

    Parameters
    ----------
    data : numpy.array
        Path to the pickled eroded speech activity database.
    thresh : int
        Maximum duration in ms of signal gaps which will be removed by erosion.
    signal : int, optional
        Determines if silence (signal=0) or speech (signal=1) should be eroded.
    columns : list(string), optional
        A list of column names which should be eroded.

    Returns
    -------
    numpy.array
        The eroded data.
    """
    res = data.copy()
    delta = (data.index[1] - data.index[0]).asm8 // 1e6
    for k in columns:
        res[k] = c5.data.fill_gaps(res[k], signal, res[k] != signal, thresh/delta.astype(int))
    return res


def window_corr(x, y, window):
    result = np.zeros(x.shape[0])
    window = int(window)
    for idx in range(window, x.shape[0]):
        a = x[idx-window:idx]
        b = y[idx-window:idx]
        result[idx] = np.sum(a*b)/float(window)
        if idx % 50000 == 0:
            logger.info('Processed {0:.2f} % of correlation data with window size {1}.'.format(idx/x.shape[0] * 100, window))
    logger.info('Processing done.')
    return result
