import cv2
import numpy as np
import logging
from os.path import exists, basename
from c5.data import peak_detection
from c5.config import STAGE2_PATH

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class VisualAnalysis:

    @staticmethod
    def detect_sync(file_name):
        hist = VisualAnalysis.calc_hist(file_name)
        y = VisualAnalysis.sync_function()
        z = VisualAnalysis.calc_channel_corr(hist, y)

        sync_at = hist[np.where(z > 2)[0], 0]
        events = {}
        last = 0
        for s in sync_at:
            if (s-last) > 10:
                events[s] = 3.0
                last = s
        return events

    @staticmethod
    def sync_function(width=8):
        framesize = 45
        pen = -1
        enh = 3
        result = np.ones((framesize, 3)) * pen
        result[0:0+width//2, 0] = enh
        result[15-width//2:15+width//2, 1] = enh
        result[15-width//2:15+width//2, 0] = 0
        result[30-width//2:30+width//2, 2] = enh
        result[30-width//2:30+width//2, 0] = 0
        result[30-width//2:30+width//2, 1] = 0
        return result

    @staticmethod
    def calc_hist(file_name):
        res = []
        capture = cv2.VideoCapture(file_name)
        idx = 0
        while capture.isOpened():
            if idx % 2 == 0:
                ret, img = capture.read()
                if img is not None:
                    r, g, b = VisualAnalysis.calc_val(img)
                    res.append((idx, r, g, b))
                else:
                    break
            else:
                capture.grab()
            idx += 1
        hist = np.array(res)
        return hist

    @staticmethod
    def calc_val(img, size=13):
        img_reduced = img
        height, width = img_reduced.shape[:2]
        img_roi = img_reduced[height//4:height//4*3, width//4:width//4*3]
        b, g, r = cv2.split(img_roi)
        hist_r = cv2.calcHist([r], [0], None, [size], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [size], [0, 256])
        hist_b = cv2.calcHist([b], [0], None, [size], [0, 256])
        return hist_r[-1], hist_g[-1], hist_b[-1]

    @staticmethod
    def sliding_window(data, size=5000, overlap=0.6):
        offset = 1 - overlap
        frames = size // 40
        tmp = np.zeros(data.shape)
        # copy timestamps to the peak result
        tmp[:, 0] = data[:, 0]
        for start in np.arange(0, data.shape[0], frames * offset, dtype=int):
            for i in range(1, 4):
                cur = np.copy(data[start:start+frames, i])
                cur /= np.ptp(cur)
                lmax, _ = peak_detection(cur, 0.75)
                if lmax.shape[0] > 0:
                    idx = lmax[:,0].astype(int)
                    idx += start
                    tmp[idx, i] = 1
        return tmp

    @staticmethod
    def calc_channel_corr(data, ref):
        corr = np.zeros((data.shape[0]-ref.shape[0]+1))
        peaks = VisualAnalysis.sliding_window(data)
        for i in range(3):
            corr += np.clip(np.correlate(peaks[:, i+1], ref[:, i], mode='valid'), a_min=0, a_max=1)
        return corr
