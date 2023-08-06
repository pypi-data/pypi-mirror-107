# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as pl
from zipfile import ZipFile
import pandas as pd

import c5.config
from c5.config import STUDIES_ACRONYMS, MARKER_IDS, arbc
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# dv camera angle unknown
# shouldnt be necessary since we can rerun with screen xcf output
# dv_matrix = np.matrix([[2.3787,0,0,0],
#                       [0,3.17159,0,0],
#                       [0,0,-1.00002,1.00136e-05],
#                       [0,0,-1,1]])
# hmd camera matrx angle 26


class KinectLoader(object):
    def __init__(self, zip_file):
        if isinstance(zip_file, int):
            zip_file = arbc.stage1.trial(zip_file).kinect_nego()
        self._zip = ZipFile(zip_file)
        files = self._zip.namelist()
        self.folder = files.pop(0)
        offset = len(self.folder) + 7
        tmp = []
        for t in files:
            # get timestamp from filename
            ts = t[offset:-4]
            if len(ts) > 0:
                tmp.append(int(ts))
        self._ts = np.array(tmp)
        self._ts.sort()
        self._idx = 0

    @property
    def timestamp(self):
        return self._ts[self._idx]

    @timestamp.setter
    def timestamp(self, value):
        idx = np.abs(self._ts - value).argmin()
        self._idx = idx

    @property
    def image(self):
        with self._zip.open("%skinect_%d.png" % (self.folder, self.timestamp)) as f:
            # image values are read as float ranging from 0 to 1.
            # To return actual distances, we have to scale values by uint16.MAX = 65535 and divide it by 10
            res = pl.imread(f) * 65535 / 10.0
        return res

    def next(self, skip=0):
        """
        Return the next image from the archive and set the timestamp accordingly.

        Attributes
        ----------
        skip : int, optional
            Skip the amount of images.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image.
        """
        self._idx += skip + 1
        if self._idx >= len(self._ts):
            raise IOError("Kinect stream ended.")
        return self.image, self._ts[self._idx]

    def forward(self, seconds):
        """
        Skip forward an amount of seconds.

        Attributes
        ----------
        seconds : int
            Amount of seconds to be skipped.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image.
        """
        goal = self.timestamp + abs(seconds * 1000)
        while self.timestamp < goal:
            self._idx += 1
        return self.image, self.ts[self.idx]

    def rewind(self, seconds=None):
        """
        Rewind an amount of seconds.

        Attributes
        ----------
        seconds : int
            Amount of seconds to rewind.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image.
        """
        if seconds is not None:
            goal = self.timestamp - abs(seconds * 1000)
            while self.timestamp > goal:
                self._idx -= 1
            return self.image, self.ts[self.idx]
        else:
            self._idx = 0

    def to_video(self, path, framerate=25):
        import cv2
        cm = pl.cm.get_cmap('jet')
        cm.set_under('k')
        img = self.image
        h, w = img.shape
        out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'X264'), framerate, (w, h))
        img[img == 0] = 1
        vmin = np.min(img)
        vmax = np.percentile(img, 20) * 1.1
        vran = vmax - vmin
        idx = 0
        off = self._ts[idx]
        dur = self._ts[-1] - off
        for time in np.arange(0, dur, 1000/framerate):
            while self._ts[idx + 1] - off < time:
                idx += 1
            with self._zip.open("%skinect_%d.png" % (self.folder, self._ts[idx])) as f:
                img = pl.imread(f) * 65535 / 10.0 - vmin
                img[img > vran] = vran
                cimg = cm(img / vran)[:, :, :3]
                out.write((cimg * 255).astype(np.uint8))
        out.release()


def collect_marker_data():
    res = {}
    for study in c5.config.STUDIES:
        # should be the second study which was F2Face
        if study == STUDIES_ACRONYMS[1]:
            continue  # no marker data available for Face-To-Face Condition
        for tid in c5.config.TRIALS[study]:
            logger.info('Collecting marker data for trial %d.', tid)
            res[tid] = _convert_marker_data(tid)
    return res


def _convert_marker_data(tid):
    logger.info("Load data for trial %d.", tid)
    conf = c5.config.ConfigLoader(tid)
    p = {}
    for m in ['hmd1', 'hmd2', 'cam3']:
        logger.info("Load data for %s.", m)
        tmp = np.loadtxt(arbc.stage1.condition(STUDIES_ACRONYMS[tid // 100 - 1]).trial(tid).file('tracker_{0}'.format(m))(),
                         dtype=c5.config.MARKER_DT)
        start = conf.get('trial.phase.negotiation.start')
        stop = conf.get('trial.phase.negotiation.stop')
        x = None
        for mid in MARKER_IDS:
            if mid < 1:
                continue
            logger.debug("Load data for marker %d", mid)
            tmp_id = tmp[tmp['id'] == mid]
            slots = c5.data.create_slots(tmp_id, start, stop).last().fillna(method='ffill')
            logger.debug("New data has %d entries", slots.shape[0])
            logger.debug("First %f, Last %f", slots.timestamp[0], slots.timestamp[-1])
            slots['delta'] = slots.index.asi8 // 1e6 - slots.timestamp
            slots.drop('id', axis=1, inplace=True)
            slots.drop('timestamp', axis=1, inplace=True)
            slots = slots.add_suffix('_m%d' % mid)
            logger.debug("Attempting to merge DataFrames")
            x = pd.DataFrame(slots) if x is None else x.join(slots)
            logger.debug("Merged")
            if not "delta_m%d" % mid in x.columns:
                raise ValueError("delta_m%d not in %s" % (mid, x.columns))
        x = x.add_suffix('_' + m)
        p[m] = x
    logger.info("Merging tracker data.")
    y = p['hmd1'].join(p['hmd2'].join(p['cam3']))
    if "delta_m111_cam3" not in y.columns:
        raise ValueError("delta_m111_cam3 not in %s" % y.columns)
    return y
