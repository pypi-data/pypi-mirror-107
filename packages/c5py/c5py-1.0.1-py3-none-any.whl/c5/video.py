import cv2
import c5.config
from c5.config import arbc

import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())


class VideoPlayer(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.cap = cv2.VideoCapture(self.file_path)
        self.buffer = []
        self.buffer_length = 20
        self.idx = 0
        self.img = None
        if self.cap.isOpened():
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.max_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            _ = self.next()
        else:
            raise Exception("ERROR: no video at %s" % self.file_path)
 
    # CV_CAP_PROP_POS_FRAMES
    # CV_CAP_PROP_POS_MSEC
    def set_timestamp(self, ms, s=0, m=0, h=0):
        timestamp = ms + s * 1e3 + m * 6e4 + h * 36e5
        self.cap.set(cv2.CAP_PROP_POS_MSEC, timestamp - 1000)
        _, tmp = self.cap.read()
        t = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        t_old = -1
        img = tmp
        while (t < timestamp - self.fps) and (t_old != t):
            img = tmp
            _, tmp = self.cap.read()
            t_old = t
            t = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def set_frame(self, frame):
        frame = max(0, self.max_frame - frame) if frame < 0 else min(frame, self.max_frame)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame-10)
        ret, tmp = self.cap.read()
        t = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        while t < frame:
            ret, tmp = self.cap.read()
            t = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.img = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)

    def get(self):
        return self.img

    @property
    def timestamp(self):
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)

    def grab(self):
        _, img = self.cap.read()
        return img

    def next(self):
        self.img = cv2.cvtColor(self.grab(), cv2.COLOR_BGR2RGB)
        return self.img


def get_video(timestamp, trial=None, view='merged'):
    conf, trial = c5.config.get_config(timestamp, trial)
    video_path = arbc.stage1.trial(trial).file("video_" + view)()
    player = VideoPlayer(video_path)
    player.set_timestamp(max(timestamp - conf.get('trial.start'), 0))
    return player


def generate_phase_video(tid, phase='negotiation', out=None):
    import subprocess
    out = out if out is not None else "{0}/trial{1}_{2}_cam3.mp4".format(
        arbc.stage2(), tid, phase)
    conf = c5.config.load_config_data(tid)
    ts_from = conf.get('trial.phase.{0}.start'.format(phase)) - conf.get('cam3.start')
    ts_to = conf.get('trial.phase.{0}.stop'.format(phase)) - conf.get('cam3.start')
    cmd = ['ffmpeg', 'i', arbc.stage1.trial(tid).file("video_cam3")(),
           '-ss', '00:{1}:{2}'.format(ts_from // 60000, ts_from % 60000 / 1000),
           '-to', '00:{1}:{2}'.format(ts_to // 60000, ts_to % 60000 / 1000),
           out]
    _LOGGER.info("Subprocess call: %s", str(cmd))
    subprocess.check_call(cmd)
