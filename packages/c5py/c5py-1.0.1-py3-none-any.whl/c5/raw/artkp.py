# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:38:03 2014

@author: alneuman
"""

from os.path import exists, join
from os import mkdir
import tempfile
import xml.sax as sax
import struct
import numpy as np
import pandas as pd
import cv2
import logging


from ..config import TRIALS, STUDIES, STUDIES_ACRONYMS, MARKER_DT, arbc, ConfigLoader, RAW_NAMES, STAGE1_NAMES

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

VELO_THRESHOLD = 1

HMD_MATRIX = np.matrix([[3.24861, 0, 0, 0],
                        [0, 4.33148, 0, 0],
                        [0, 0, -1.00002, 1.00136e-05],
                        [0, 0, -1, 1]])


def check(trial):
    logger.info("Checking for trial %d data at '%s'", trial, arbc.raw.trial(trial)())
    cfg = exists(arbc.raw.trial(trial).config_json())
    hmd = exists(arbc.raw.trial(trial).tracker_hmd())
    cam = exists(arbc.raw.trial(trial).tracker_top())
    return cfg and hmd and cam


def filter_data(data, threshold, limit=3):
    if isinstance(data, np.ndarray):
        cleared = pd.DataFrame.from_records(data)
    else:
        cleared = data.copy()
    mids = cleared.id.unique()
    for mid in mids:
        d = cleared[cleared.id == mid]
        if d.shape[0] > 0:
            count = 0
            drops = [None]
            while count != limit and len(drops) > 0:
                d = cleared[cleared.id == mid]
                dx = (d.s_x.diff() / d.timestamp.diff()).abs()
                dy = (d.s_y.diff() / d.timestamp.diff()).abs()
                drops = d[((dx > threshold) | (dy > threshold))].index.tolist()
                cleared.loc[drops, 'id'] = 0
                count += 1

    clear_idx = cleared[cleared.id == 0].index.tolist()
    cleared.drop(cleared.index[clear_idx], inplace=True)
    return cleared, len(clear_idx)


class RegionExtractor(object):
    def __init__(self):
        self.points = [(0, 0), (1920, 1080)]
        self.idx = 0
        self.img = None

    def mouse_up(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            logger.debug("%d:%d", x, y)
            if y < 10:
                y = 0
            elif y > 1070:
                y = 1080
            self.points[self.idx] = (x, y)

    def draw(self):
        img2 = self.img.copy()
        cv2.rectangle(img2, self.points[0], self.points[1], (0, 255, 0), 3)
        if self.idx == 0:
            text = "Click top left table corner.\nClick 'm' to proceed."
        else:
            text = "Click bottom right table corner.\nClick 'm' to finish and\n'n' to reset top left corner."
        font = cv2.FONT_HERSHEY_SIMPLEX
        for idx, line in enumerate(text.split('\n')):
            cv2.putText(img2, line, (50, 50 + idx * 50), font, 1,  
                        (0, 255, 0), 2, cv2.LINE_4)
        cv2.imshow('image', img2)

    def extract(self, path):
        cap = cv2.VideoCapture(path)
        if cap.isOpened():
            ret, self.img = cap.read()
        else:
            logger.error("No video at %s", path)
        self.draw()
        cv2.setMouseCallback('image', self.mouse_up)
        while True:
            if self.idx < 0:
                self.idx = 0
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                self.idx += 1
            elif k == ord('n'):
                self.idx -= 1
            elif k == ord('x'):
                ret, self.img = cap.read()
                cv2.imshow('image', self.img)
            # we ignore the inner rectangle, otherwise 1 should be 3
            elif k == 27 or self.idx > 1:
                break
            self.draw()
        cap.release()
        cv2.destroyWindow('image')
        return self.points


def load_xcf_log(filename, time=None, matrix=None, res_x=None, res_y=None):
    if exists(filename) is False:
        return None
    tmp_fd, tmp_path = tempfile.mkstemp()
    tmp_file = open(tmp_path, 'w')
    tmp_file.write("<LAFORGE>\n")
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('<MARKER') and line.endswith("MARKERLIST>\n"):
                tmp_file.write(line)
    tmp_file.write("</LAFORGE>\n")
    tmp_file.close()
    handler = XcfHandler(time, matrix, res_x, res_y)
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(tmp_path)
    data = handler.result()
    res = {}
    for key, value in data.items():
        if '/' in key:
            key = key.split('/')[-2]
            key += "_artkp"
            if "trial" in key:
                key = "cam3_artkp"
        res[key] = np.array(value, dtype=MARKER_DT)
    return res


class XcfHandler(sax.handler.ContentHandler):
    def __init__(self, time=None, matrix=None, res_x=None, res_y=None):
        self.time_cue = struct.pack("L", time)[4:] if time is not None else None
        self.timeframe = {}
        self.active = None
        self.timestamp = None
        self.generator = None
        self.matrix = matrix
        self.res_x = res_x
        self.res_y = res_y
        self._result = {}
        # ignore origin parameters
        self.is_origin = False

    def startElement(self, name, attrs):
        if name == "UPDATED":
            value = attrs["value"]
            # bugfix:
            # some versions of the position_logger have a bug where the uint64
            # timestamp is broken and only the first 4 byte are written.
            # Luckily these false timestamps can be identified by the suffix
            # which is 'll'. To repair these values we require a valid uint64
            # timestamp from the trial. Any value from the configuration or the
            # sync event should be valid.
            if 'll' in value:
                if self.time_cue is None:
                    raise ValueError("Broken timestamp detected but no time cue was passed.")
                value = struct.pack('I', int(value[:-2])) + self.time_cue
                value = struct.unpack('L', value)[0]
                #print value
            self.timestamp = value
        elif name == "GENERATOR":
            self.generator = ""
        elif name == "MARKERCOORDINATES":
            # new coordinates, delete old data except timestamp
            m_data = ['p_x', 'p_y', 'p_z', 'o_w', 'o_x', 'o_y', 'o_z',
                      's_x', 's_y']
            for k in m_data:
                if k in self.timeframe:
                    self.timeframe.pop(k)
            self.timeframe = {}
            self.timeframe['id'] = attrs['id']
        elif name == "POINT3D" and self.is_origin is False:
            self.timeframe['p_x'] = attrs['x']
            self.timeframe['p_y'] = attrs['y']
            self.timeframe['p_z'] = attrs['z']
            if self.matrix is not None:
                pos = np.array([float(attrs['x']), float(attrs['y']),
                                float(attrs['z']), 1])
                # TODO: this needs to be extracted from the call
                screen = self.convertSceneToScreenPosition(
                    pos, self.matrix, self.res_x, self.res_y)
                self.timeframe['s_x'] = screen[0]
                self.timeframe['s_y'] = screen[1]
        elif name == "POINT2D" and self.is_origin is False and self.matrix is None:
            self.timeframe['s_x'] = float(attrs['x'])
            self.timeframe['s_y'] = float(attrs['y'])
        elif name == "QUATERNION" and self.is_origin is False:
            self.timeframe['o_w'] = attrs['w']
            self.timeframe['o_x'] = attrs['x']
            self.timeframe['o_y'] = attrs['y']
            self.timeframe['o_z'] = attrs['z']
        elif name == "ORIGIN":
            self.is_origin = True
        self.active = name

    def characters(self, content):
        if self.active == "GENERATOR":
            self.generator += content

    def endElement(self, name):
        if name == "MARKERCOORDINATES":
            # skip invalid data
            # we know the data is invalid since 0 is the point of origin
            if self.timeframe['p_x'] == 0:
                return
            self.timeframe['timestamp'] = self.timestamp
            # Normalize Data if the resolution was supplied
            if self.res_x is not None:
                self.timeframe['s_x'] /= self.res_x
                self.timeframe['s_y'] /= self.res_y
            row = []
            for field in MARKER_DT.names:
                row.append(self.timeframe[field])
            self._result.setdefault(self.generator, []).append(tuple(row))
        elif name == "ORIGIN":
            self.is_origin = False

    def result(self):
        return self._result

    def convertSceneToScreenPosition(self, pos, matrix, width, height):
        rel_pos = np.squeeze(np.asarray(np.dot(matrix, pos)))
        rel_pos_unit = rel_pos / rel_pos[3]
        result = np.zeros(2)
        result[0] = (0.5 + 0.5 * rel_pos_unit[0]) * width
        result[1] = (0.5 - 0.5 * rel_pos_unit[1]) * height
        return result


def _write_data(data, path="./out.csv"):
    if exists(path):
        logger.warning("File %s already exists. It will not be overwritten." % path)
        return
    np.savetxt(path, data,
               fmt=['%d'] * 2 + ['%.3f'] * 9, delimiter=" ",
               header=", ".join(MARKER_DT.names), comments='#')


def _arbaseline_remapping(data):
    if isinstance(data, np.ndarray):
        data = pd.DataFrame.from_records(data)
    # remove entries without ids
    data = data.drop(data[data.id == 0].index)
    # remap
    id_map = {47: 6, 42: 20, 137: 24, 20: 42, 6: 47, 24: 137}
    tmp = {}
    # we have to iterate twice to not accidentally override IDs later
    for k in id_map:
        tmp[k] = data.id == k
    for k, idx in tmp.items():
        data.loc[idx, 'id'] = id_map[k]
    return data


def convert_data(trial, path=None, out='.'):
    logger.info("Process trial {0}".format(trial))
    # load tracker data
    path = arbc.raw.trial(trial)() if path is None else path
    filename = join(path, RAW_NAMES['config_json'].format(tid=trial))
    identifier = filename if exists(filename) else trial
    con = ConfigLoader(identifier)

    # hmd1.start should be roughly the time when the system was started
    time = con.get("hmd1.start")
    # study 1 lacks screen information
    matrix = HMD_MATRIX if trial < 200 else None
    logger.info("Loading data...")
    tracker = dict()
    hmd_filepath = join(path, RAW_NAMES['tracker_hmd'].format(tid=trial))

    if exists(hmd_filepath):
        if not out or \
            (not exists(join(out, STAGE1_NAMES['tracker_hmd1'].format(tid=trial))) and
             not exists(join(out, STAGE1_NAMES['tracker_hmd2'].format(tid=trial)))):
            hmd = load_xcf_log(hmd_filepath, time, matrix, 800, 600)
            tracker['artkp_hmd1'] = hmd['lt3_artkp']
            tracker['artkp_hmd2'] = hmd['lt2_artkp']
            if 'lt1_artkp' in hmd:
                tracker['artkp_top'] = hmd['lt1_artkp']
        else:
            logger.info("Output files for hmd already exists. Skip conversion.")
    else:
        logger.warn("HMD files not found!")

    top_filepath = join(path, RAW_NAMES['tracker_top'].format(tid=trial))
    if exists(top_filepath):
        if not out or not exists(join(out, STAGE1_NAMES['tracker_cam3'].format(tid=trial))):
            cam = load_xcf_log(top_filepath, time)
            if len(cam) != 1:
                raise Exception("something went wrong with cam3 tracker")
            data, cleared = filter_data(list(cam.values())[0], VELO_THRESHOLD)
            logger.info("Removed {0} entries from data set".format(cleared))
            # normalize table data
            if out:
                ext = RegionExtractor()
                points = ext.extract(arbc.stage1.trial(trial).video_cam3())
                data['s_x'] -= points[0][0]
                data['s_x'] /= (points[1][0] - points[0][0])
                data['s_y'] -= points[0][1]
                data['s_y'] /= (points[1][1] - points[0][1])
                tracker['artkp_cam3'] = data
        else:
            logger.info("Output file for cam3 already exists. Skip conversion.")
    else:
        logger.warn("Top camera files not found")

    # write data
    if out:
        for generator in tracker:
            out_path = "%s/trial%d_%s.csv" % (out, trial, generator)
            logger.info("Writing data to " + out_path)
            if not exists(out_path):
                # during the first study another marker id mapping was used
                if trial // 100 == 1:
                    logger.info("remap IDs...")
                    tracker[generator] = _arbaseline_remapping(tracker[generator])
                _write_data(tracker[generator], out_path)
            else:
                logger.warn("Output file %s already exists. It will not be overwritten.", out_path)
    else:
        logger.info('No out path specified. Data will not be written.')


def start_app(args=None):
    if args[0] in ['convert', 'test']:
        out = './out' if args[0] == 'convert' else ''
        if 'all' in args[1]:
            dic = TRIALS
        else:
            tid = int(args[1])
            dic = {STUDIES[STUDIES_ACRONYMS[tid//100-1]]: [tid]}
        for study, trials in dic.items():
            # skip 2nd study since no markers were used
            if "NoAR" in study:
                continue
            for trial in trials:
                if check(trial) is False:
                    logger.error("Data missing for trial %d. Abort", trial)
                if out and exists(out) is False:
                    mkdir(out)
                convert_data(trial, out=out)
    elif exists(args[0]):
        path = args[0]
        for study, trials in TRIALS.items():
            # skip 2nd study since no markers were used
            if "NoAR" in study:
                continue
            for trial in trials:
                if exists('./out') is False:
                    mkdir('./out')
                convert_data(path, trial, './out')
