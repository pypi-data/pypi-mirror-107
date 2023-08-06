from c5.config import TRIALS, TRIAL_IDS
from c5.sensors import KinectLoader
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

BLOB_TD = [('timestamp', 'u8'), ('speaker', 'u4'), ('area', 'f8'), ('centerx', 'f8'),
           ('centery', 'f8'), ('arc', 'f8'), ('x', 'f8'), ('y', 'f8'), ('w', 'f8'), ('h', 'f8')]

INTERVAL = 1000
RATE = 1


def collect_user_blobs(stepsize=10, threshold=0, progress_callback=None):
    db = {}
    counter = 0
    for study, trials in TRIALS.items():
        for tid in trials:
            # for trial 107, no Kinect data have been recorded
            if tid == 107:
                counter += 1
                continue
            db[tid] = generate_user_blobs(KinectLoader(tid), stepsize, threshold)
            counter += 1
            if progress_callback is not None:
                progress_callback(counter/len(TRIAL_IDS))
    return db


def generate_user_blobs(loader, stepsize, threshold=None):
    blobs = []
    try:
        while True:
            x, ts = loader.next(stepsize - 1)
            blob = _get_blobs(x, threshold)
            while len(blob) != 16 or blob[1] > 320 or blob[9] < 320:
                logger.debug("Blob info invalid. Using next frame.")
                x, ts = loader.next()
                blob = _get_blobs(x, threshold)
            for i in range(2):
                res = [ts, i]
                res.extend(blob[i * 8:i * 8 + 8])
                # has to be converted into tuple for fromrecords to work
                blobs.append(tuple(res))
    except IOError:
        pass
    return np.rec.fromrecords(blobs, dtype=BLOB_TD)


def _get_blobs(img, threshold):
    y = np.copy(img)
    low = y > threshold
    y[low] = 0
    tmp = find_user_area(y)
    return tmp


def get_heatmap(kin, threshold, stepsize=50):
    kin.rewind()

    x, ts = kin.next()
    z = np.zeros(x.shape)
    try:
        while True:
            y = np.zeros(x.shape)
            x, ts = kin.next(stepsize-1)
            x[x > threshold] = 0
            b = np.array(x, dtype=np.uint8)
            contours, hierarchy = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            contours = sorted(contours, key=lambda con: con.shape[0], reverse=True)[:2]
            cv2.drawContours(y, contours, -1, (1, 0, 0), -1)
            z += y
    except IOError:
        pass
    return z


def find_user_area(img):
    tmp = np.array(img * 255, dtype=np.uint8)
    contours, hierarchy = cv2.findContours(tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    res = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            continue
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        area = cv2.contourArea(cnt)
        arc = cv2.arcLength(cnt, True)
        x, y, w, h = cv2.boundingRect(cnt)
        res.append([area, cx, cy, arc, x, y, w, h])

    # take the two largest blobs...
    res = sorted(res, key=lambda con: con[0], reverse=True)[:2]
    # sort them by x position to have the left person always first
    res = sorted(res, key=lambda con: con[1])
    return np.array(res).flatten()
