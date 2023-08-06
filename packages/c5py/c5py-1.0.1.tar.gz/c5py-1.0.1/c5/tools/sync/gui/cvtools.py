import cv2
import os.path

from PyQt5.QtGui import QImage
from os.path import exists
import numpy as np


import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NpQImage(QImage):

    def __init__(self, frame, frame_nr):
        height, width, channel = frame.shape
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bytes_per_line = 3 * width
        self._data = frame
        self._frame = frame_nr
        super(NpQImage, self).__init__(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

    def get_frame(self):
        return self._frame

    def as_array(self):
        return self._data


class CVVideo:
    def __init__(self, parent=None):
        self._buffer = {}
        self._store = {}
        self.parent = parent
        self._capture = None
        self._frame = None
        self._image = None
        self._current = -1
        self.path = ""

    def set_capture(self, path):
        self._capture = cv2.VideoCapture(path)
        # Take one frame to query dimension
        ret, frame = self._capture.read()
        if not ret:
            raise IOError("Could not load frame.")
        self._frame = np.zeros(frame.shape, np.uint8)
        self._image = self._build_image(frame)
        self._current = self._image.get_frame()
        self.path = path

    def _build_image(self, frame):
        return NpQImage(frame, self._get_current_frame())

    def _get_current_frame(self):
        return self._capture.get(cv2.CAP_PROP_POS_FRAMES)

    def get_current_frame(self):
        if self._current < 0:
            return self._get_current_frame()
        else:
            return self._current

    def store_images(self, frame_list):
        self._store.clear()
        for nr in frame_list:
            self.set_current_frame(nr, show=False)
            try:
                self._store[nr] = self._buffer[nr]
            except KeyError:
                logger.warn("Frame %d could not be retrieved!", nr)
        return self._store

    def save_images(self, frame_list, destination):
        filename = os.path.basename(self.path)
        frame_list = sorted([frame for frame in frame_list
                             if not exists("%s/%s.%i.png" % (destination, filename, frame))])
        imgs = self.store_images(frame_list)
        for frame, img in imgs.items():
            path = "%s/%s.%i.png" % (destination, filename, frame)
            if not exists(path):
                img.save(path, "PNG")
            else:
                logger.info("%s already exists", path)

    def set_current_frame(self, value, show=True):
        logger.info("Go to frame %d", value)
        if value > self._capture.get(cv2.CAP_PROP_FRAME_COUNT):
            logger.error("Frame index %d exceeds video frame count!", value)
            return

        if value not in self._buffer.keys():
            self._buffer.clear()
            frame_number = max(0, value - 100)
            self._capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            logger.debug("Current frame: %d", self._get_current_frame())
            self._capture.read()
            while self._get_current_frame() > (value - 50):
                frame_number = max(0, frame_number-1)
                self._capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                self._capture.read()
                logger.debug("Rewind to frame %d", frame_number)
            while self._get_current_frame() < (value - 50):
                self._capture.read()
            for i in range(100):
                ret, frame = self._capture.read()
                self._buffer[self._get_current_frame()] = self._build_image(frame)

        self._current = value
        if show is True:
            self._image = self._buffer[self._current]
            if self.parent is not None:
                self.parent.update()

    def frame_step(self, reverse=False):
        if reverse is True:
            self._current -= 1
        else:
            self._current += 1

        if self._current not in self._buffer.keys():
            self.set_current_frame(self._current)
        else:
            self._image = self._buffer[self._current]
            if self.parent is not None:
                self.parent.update()

    def get_current_image(self):
        return self._image
