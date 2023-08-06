from os.path import exists, dirname
import logging

import numpy as np
import pandas as pd
import cv2

from c5.config import SAMPLING_INTERVAL
from c5.video import VideoPlayer
from c5.elan import ElanReader

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())


class ProcessingHandler(object):
    handlers = {}

    def __init__(self, caller=None, func=None):
        self.context = caller.context if caller is not None else {}
        self._func = func if func is not None else lambda: {}

    def __call__(self, *args, **kwargs):
        kwargs.update(self.context)
        new_vals = self._func(*args, **kwargs)
        self.context.update(new_vals)
        return self

    def __getattribute__(self, item):
        handlers = super(ProcessingHandler, self).__getattribute__('handlers')
        if item in handlers:
            return ProcessingHandler(self, handlers[item])
        return super(ProcessingHandler, self).__getattribute__(item)


def process(*args, **kwargs):
    return ProcessingHandler(**kwargs)


def load_eaf(elan_file, trial_id=None, tier_regex=None, **kwargs):
    elan_reader = ElanReader(elan_file, trial_id)
    tmp = pd.DataFrame(elan_reader.data).drop('content', axis=1)
    _LOGGER.info("Loaded %d rows", tmp.shape[0])
    if tier_regex:
        tmp = tmp[tmp.tier.str.startswith(tier_regex)]
        _LOGGER.info("Tier filter returned %d rows", tmp.shape[0])
    return dict(classes=sorted(tmp.tier.unique()), sequences=tmp)


def load_sequences(sequences, field='class'):
    return dict(classes=sequences[field].unique(), sequences=sequences)


def filter_duration(sequences, min_duration=0, max_duration=None, **kwargs):
    max_duration = sequences.duration.max() if max_duration is None else max_duration
    sequences = sequences[sequences.duration.between(min_duration, max_duration, inclusive=True)]
    _LOGGER.info("Duration filter returned %d rows", sequences.shape[0])
    return dict(sequences=sequences, max_duration=max_duration)


def padded(*args, **kwargs):
    _LOGGER.info("Configure padding")
    return dict(padded=True)


def add_reject(sequences, classes, max_duration=None, padded=None, **kwargs):
    _LOGGER.info("Adding reject samples")
    reject = get_reject_samples(sequences, max_duration, pad=padded)
    sequences = sequences.append(reject, ignore_index=True, sort=False)
    _LOGGER.info("Data set now contains %d rows", sequences.shape[0])
    return dict(sequences=sequences, classes=classes.append('reject'))


def from_video(video_file, sequences, offset=0, **kwargs):
    sequences.start += offset
    return dict(video=VideoPlayer(video_file), image_hooks=[])


def crop(video, image_hooks, x=0, y=0, width=None, height=None, **kwargs):
    width = int(video.width) if width is None else width
    height = int(video.height) if height is None else height
    _LOGGER.info("Adding cropping image hook (x=%d, y=%d, width=%d, height=%d)", x, y, width, height)

    def crop_img(img):
        return img[y:y + height, x:x + width]

    image_hooks.append(crop_img)
    return dict(image_hooks=image_hooks)


def write_videos(video_prefix, video, sequences, video_format='mp4',
                 image_hooks=None, override=False, **kwargs):
    image_hooks = [] if image_hooks is None else image_hooks
    _LOGGER.info('Processing video writing to %s', dirname(video_prefix))
    for idx, row in sequences.iterrows():
        fname = "{0}_{1}_{2}.{3}".format(video_prefix, idx, row.tier, video_format)
        _LOGGER.debug('Writing video %s', fname)
        if not exists(fname) or override:
            # check dimension of the resulting image
            img = video.grab()
            for hook in image_hooks:
                img = hook(img)
            width, height = img.shape[1], img.shape[0]
            _LOGGER.debug('Output parameters: fps=%f, width=%d, height=%d, duration=%d ms',
                          video.fps, width, height, row.duration)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(fname, fourcc, video.fps, (width, height))
            start = row.start
            stop = row.start + row.duration
            video.set_timestamp(start)
            while video.timestamp <= stop:
                img = video.grab()
                for hook in image_hooks:
                    img = hook(img)
                writer.write(img)
            writer.release()
    return dict(sample_path=dirname(video_prefix))


ProcessingHandler.handlers = {
    'load_eaf': load_eaf,
    'filter_duration': filter_duration,
    'padded': padded,
    'add_reject': add_reject,
    'from_video': from_video,
    'crop': crop,
    'write_videos': write_videos
}


def get_reject_samples(df, max_duration=6000, pad=False, fps=SAMPLING_INTERVAL):
    df = df.assign(stop=df.timestamp + df.duration)
    no_dups = df.drop(df[((df.timestamp.shift(-1) - df.stop) < 0).shift(1).fillna(False)].index)
    values = df.shape[0] // 2
    # get all phases where no gesture is annotated
    empty = pd.DataFrame(dict(timestamp=no_dups.stop, stop=no_dups.timestamp.shift(-1),
                              duration=no_dups.timestamp.shift(-1) - no_dups.stop, tier='none'))
    empty = empty[empty.duration > max_duration * 1.25]
    empty = pd.DataFrame(dict(start=empty.timestamp + 0.25, stop=empty.stop))
    empty_start = np.array([])
    for idx, r in empty.iterrows():
        # define the range of possible start values for the reject samples which is the difference
        # between the filtered duration and the max duration of a sequence
        empty_start = np.concatenate([empty_start, np.arange(r.start, r.stop - max_duration, fps)])
    empty_start = pd.Series(empty_start)

    try:
        # in case of padding, we take the maximum duration
        if pad:
            ts, dur = empty_start.sample(values).values, max_duration
        else:
            # otherwise we take actually observed durations to prevent fitting on sequence durations
            ts, dur = empty_start.sample(values).values, df.duration.sample(values).values
    except ValueError:
        ts = empty_start.sample(values, replace=True).values
        dur = max_duration
    # calculate the video time based on the offset value from the reference data 'df'
    offset = df.iloc[0].timestamp - df.iloc[0].start
    empty = pd.DataFrame(dict(timestamp=ts, duration=dur, start=ts-offset, tier='reject'))
    return empty
