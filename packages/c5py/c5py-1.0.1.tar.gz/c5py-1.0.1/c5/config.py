# -*- coding: utf-8 -*-

import json
import collections
import numpy as np
import sys
import os.path
import pickle

SAMPLING_RATE = 25  # Hz
SAMPLING_INTERVAL = 1000 // SAMPLING_RATE  # 40 ms


# Names
STAGE1_PATH = os.environ["C5_STAGE1_PATH"] if "C5_STAGE1_PATH" in os.environ else '.'
RAW_PATH = os.environ["C5_RAW_PATH"] if "C5_RAW_PATH" in os.environ else '.'
STAGE2_PATH = os.environ["C5_STAGE2_PATH"] if "C5_STAGE2_PATH" in os.environ else '.'
EXTRA_PATH = os.environ["C5_EXTRA_PATH"] if "C5_EXTRA_PATH" in os.environ else '.'


CONFIG_PATH = "{0}/meta.pkl"

MARKER_DT = np.dtype({
    'names': ['timestamp', 'id', 'p_x', 'p_y', 'p_z',
              'o_w', 'o_x', 'o_y', 'o_z', 's_x', 's_y'],
    'formats': [np.uint64, np.uint, np.float, np.float, np.float,
                np.float, np.float, np.float, np.float, np.float, np.float]})

MARKER_ACRONYMS = {1: "HAB", 4: "BBQ", 6: "QP", 11: "BR", 19: "CP", 20: "MG",
                   24: "WPA", 42: "FS", 47: "BD", 50: "SP", 53: "PZ", 64: "NPA", 70: "RC",
                   80: "WP", 111: "Compass", 137: "H", 171: "WS", 212: "KT", 220: "NT"}

ACRONYM_IDS = {v: k for k, v in MARKER_ACRONYMS.items()}

MARKER_NAMES = {1: "Hot Air Balloon", 4: "BBQ", 6: "Quad Park", 11: "Bridge", 19: "Car Park", 20: "Minigolf",
                24: "Water Protection Area", 42: "Fish Sign", 47: "Bird Sign", 50: "Skater Park", 53: "Petting Zoo",
                64: "Nature Protection Area", 70: "Ropes Course", 80: "Waterpark/Playground", 111: "Compass",
                137: "Hotel", 171: "Water Ski", 212: "Kids Train", 220: "Nature Trail"}

MARKER_IDS = sorted(MARKER_ACRONYMS.keys())

BRIX_DT = np.dtype({'names': ['timestamp', 'gyrox', 'gyroy', 'gyroz', 'accx', 'accy', 'accz'],
                    'formats': ['i8', 'i4', 'i4', 'i4', 'i4', 'i4', 'i4']})

INERTIAL_DT = np.dtype({'names': ['timestamp', 'gyrox', 'gyroy', 'gyroz', 'accx', 'accy', 'accz'],
                        'formats': ['i8', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4']})

MARKER_DELTA_DT = np.dtype(MARKER_DT.descr +
                           np.dtype([('delta', np.uint64)]).descr)
BRIX_DELTA_DT = np.dtype(BRIX_DT.descr +
                         np.dtype([('delta', np.uint64)]).descr)
                     
DTYPE_DEFAULTS = {np.dtype('uint64'): np.nan,
                  np.dtype('<U22'): '',
                  np.dtype('float64'): np.nan}

STAGES = ['raw', 'stage1', 'stage2', 'extra']

STUDIES = {'ARBase': "2011-12_ARBaseline",
           'F2Face': "2012-04_NoARBaseline",
           'ARPre': "2013-04_ARPre",
           'ARAssist': "2013-07_ARAssistance",
           'ARInter': "2014-04_ARInterception"}

# this only works as long as folders in STUDIES are prefixed with dates
STUDIES_FOLDER = sorted(STUDIES.values())
STUDIES_ACRONYMS = [k for (k, v) in sorted(STUDIES.items(), key=lambda x: x[1])]

SYNC_XML = {
    '2011-12_ARBaseline': "c5_AR.xml",
    '2012-04_NoARBaseline': "c5_NoAR.xml",
    '2013-04_ARPre': "c5_ARPre.xml",
    '2013-07_ARAssistance': "c5_ARAss.xml",
    '2014-04_ARInterception': "c5_ARInt.xml"
}

TRIALS = {
    'ARBase': list(range(101, 111)),
    'F2Face': list(range(201, 213)),
    'ARPre': list(range(301, 306)),
    'ARAssist': list(range(401, 416)),
    'ARInter': list(range(501, 516))
}

TRIAL_IDS = sorted(sum(TRIALS.values(), []))

# raw
RAW_NAMES = {
    'config_json': "trial{tid}.json",
    'video_ogv_hmd1': "trial{tid}_hmd1.ogv",
    'video_ogv_hmd2': "trial{tid}_hmd2.ogv",
    'video_dv_cam1': "VP_Gruppe_{tid}/cam_1/AVCHD",
    'video_dv_cam2': "VP_Gruppe_{tid}/cam_2/AVCHD",
    'video_dv_cam3': "VP_Gruppe_{tid}/cam_3/AVCHD",
    'brix_log_s1': "trial{tid}_brix_s1.log",
    'brix_log_s2': "trial{tid}_brix_s2.log",
    'brix_sync': "trial{tid}_sync1.log",
    'tracker_hmd': "trial{tid}_hmd.xml",
    'tracker_top': "trial{tid}_cam3.xml",
    'kinect_old': "trial{tid}_kinect.zlib",
    'kinect_new': "trial{tid}_kinect.c5k",
    'mic_wav': "trial{tid}_mic.wav"
}

# preprocessed
STAGE1_NAMES = {
    'video_cam1': "trial{tid}_cam1.mp4",
    'video_cam2': "trial{tid}_cam2.mp4",
    'video_cam3': "trial{tid}_cam3.mp4",
    # 'video_mp4_hmd1': "trial{tid}_hmd1.mp4" // hmd videos are not included because of their wrong timing
    # 'video_mp4_hmd2': "trial{tid}_hmd2.mp4" // if required, they should be cropped from the merged video
    'video_merged': "trial{tid}.mp4",
    'config_json': "trial{tid}.json",
    'ca_deixis': "trial{tid}_dG.eaf",
    'ca_structure': "trial{tid}_zE.eaf",
    'ca_gaze': "trial{tid}_MutualGaze.eaf",
    'ca_features': "trial{tid}_final.eaf",
    'tracker_hmd1': "trial{tid}_artkp_hmd1.csv",
    'tracker_hmd2': "trial{tid}_artkp_hmd2.csv",
    'tracker_cam3': "trial{tid}_artkp_cam3.csv",
    'brix_s1': "trial{tid}_brix_s1.csv",
    'brix_s2': "trial{tid}_brix_s2.csv",
    'kinect_free': "trial{tid}_kinect_free.zip",
    'kinect_nego': "trial{tid}_kinect_negotiation.zip",
    'kinect_pres': "trial{tid}_kinect_presentation.zip",
    'mic_wav': "trial{tid}_mic.wav"
}

STAGE2_NAMES = {
    'kinect_nego_video': 'trial{tid}_kinect_nego.mp4',
    'speech_activity': 'speech_activity.h5',
    'speech_activity_eroded': 'speech_activity_eroded.h5',
    'speech_activity_map': 'speech_activity_map.png',
    'speech_activity_trial': 'trial{tid}_speech_activity.csv',
    'turns': 'speech_activity_turns.pkl',
    'object_visibility': 'marker_visibility.h5',
    'object_visibility_trial': 'trial{tid}_marker_vis.csv',
    'participant_space': 'participant_blobs.pkl',
    'head_orientation': 'head_orientation.pkl',
    'marker_data': 'marker_data.h5',
}

FILE_NAMES = dict(list(RAW_NAMES.items()) + list(STAGE1_NAMES.items()) + list(STAGE2_NAMES.items()))


class ConfigLoader:
    #  DIRECTORY = 1;    MERGED_VIDEO = 2
    #  CAM1_VIDEO = 3;    CAM1_START = 4;    CAM2_VIDEO = 5;    CAM2_START = 6
    #  CAM3_VIDEO = 7;    CAM3_START = 8;    HMD1_VIDEO = 9; HMD2_VIDEO = 11;
    #  MIC = 13;

    def __init__(self, trial=None):
        self._data = {}
        if isinstance(trial, int):
            trial = arbc.stage1.trial(trial).config_json()
        if trial is not None:
            self.load(trial)

    def load(self, filename):
        with open(filename, 'r') as f:
            self._data = json.load(f)

    def data(self):
        return self._data

    def has_element(self, path):
        return self._step_down(self._data, path.split('.')) is not None

    def get(self, path):
        return self._step_down(self._data, path.split('.'))

    def set(self, path, value):
        return self._step_down(self._data, path.split('.'), value)

    def save(self, filename, overwrite=False):
        if os.path.exists(filename) and not overwrite:
            print("file exists")
            return False
        with open(filename, 'w') as f:
            json.dump(self._data, f, indent=4, sort_keys=True)
            return True

    def _step_down(self, elem, path, value=None):
        if isinstance(elem, collections.Iterable):
            if len(path) > 1:
                key = path.pop(0)
                if key in elem:
                    return self._step_down(elem[key], path, value)
                elif value is not None:
                    elem[key] = {}
                    return self._step_down(elem[key], path, value)
            elif len(path) == 1:
                key = path.pop(0)
                if value is not None:
                    elem[key] = value
                return elem[key]
        return None


class Resolver(object):
    _prefix = ''

    def __init__(self, value='', parent=None):
        self._value = value
        self._parent = parent

    def __getattribute__(self, item):
        if item.startswith("_"):
            return super(Resolver, self).__getattribute__(item)
        elif item in STAGES + StageResolver._kws:
            return StageResolver(item, self)
        elif item in list(STUDIES.keys()) + ConditionResolver._kws:
            return ConditionResolver(item, self)
        elif item.startswith('trial'):
            return TrialResolver(item, self)
        else:
            return FileResolver(item, self)

    def __call__(self, arg=None, **kwargs):
        if arg is not None:
            self._value = self._prefix + str(arg)
            return self
        elif self._parent is not None:
            return self._parent() + self._resolve(**kwargs)
        else:
            return ""

    def _resolve(self):
        return self._value

    def __dir__(self):
        return list(STAGES)


class StageResolver(Resolver):
    _kws = ['stage']

    def _resolve(self):
        if self._value in self._kws:
            return ''
        return dict(raw=RAW_PATH, stage1=STAGE1_PATH, stage2=STAGE2_PATH, extra=EXTRA_PATH)[self._value]

    def __dir__(self):
        if self._value in STAGES[2:]:
            t = s = []
        else:
            t = ['trial' + str(tid) for tid in TRIAL_IDS]
            s = list(STUDIES.keys())
        return s + t + self._list_files()

    def _list_files(self, tid_set=False):
        return list(dict(raw=RAW_NAMES.keys() if tid_set else [],
                         stage1=STAGE1_NAMES.keys() if tid_set else [],
                         stage2=STAGE2_NAMES.keys())[self._value])


class ConditionResolver(Resolver):
    _kws = ['condition']

    def _resolve(self):
        val = ''
        if self._value not in self._kws:
            try:
                val = '/' + STUDIES[self._value]
            except KeyError:
                val = '/' + STUDIES_FOLDER[self._value - 1]
        return val

    def __dir__(self):
        t = ['trial' + str(tid) for tid in TRIALS[self._value]] if self.parent._value not in STAGES[2:] else []
        return t + self._parent._list_files()


class TrialResolver(Resolver):
    _prefix = 'trial'

    def _resolve(self):
        if self._value == self._prefix:
            return ''
        elif isinstance(self._parent, StageResolver) and self._parent._value in STAGES[:2]:
            return ConditionResolver(self._get_tid() // 100,
                                     self._parent)._resolve() + "/" + self._value
        elif isinstance(self._parent, ConditionResolver) or isinstance(self._parent, ConditionResolver):
            if self._get_tid() not in TRIALS[self._parent._value]:
                raise AttributeError("Trial is not part of the chosen condition!")
        return '/' + self._value

    def _get_tid(self):
        return int(self._value[len(TrialResolver._prefix):])

    def __dir__(self):
        l = self._parent if isinstance(self._parent, StageResolver) else self._parent._parent
        return l._list_files(True)


class FileResolver(Resolver):

    def _resolve(self, format_string=True):
        d = {}
        if isinstance(self._parent, TrialResolver):
            d['tid'] = self._parent._get_tid()
            d['tid_short'] = d['tid'] % 100
        ret = '/' + FILE_NAMES[self._value]
        if format_string:
            try:
                ret = ret.format(**d)
            except KeyError:
                raise AttributeError("Resolving file name requires trial information. Please add this to your path.")
        return ret


def get_config(timestamp, trial_id=None):
    if trial_id is not None:
        return ConfigLoader(trial_id), trial_id
    for study in STUDIES:
        for tid in TRIALS[study]:
            conf = ConfigLoader(tid)
            if conf.get('trial.stop') > timestamp:
                return conf, tid
    return None, None


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if not os.path.exists(argv[1]):
        print("%s does not exist" % argv[1])
        return
    loader = ConfigLoader(argv[1])
    if loader.has_element("hmd1.start"):
        loader.set("hmd1.test", 1337)
        loader.set("hmd1.test2", "teststring")
        loader.set("hmd1.start.test", 1)
    else:
        print("path not found")


def load_config_data(path=None):
    path = path if path is not None else CONFIG_PATH.format(STAGE2_PATH)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            meta = pickle.load(f)
    else:
        meta = {}
        for s in STUDIES:
            for t in TRIALS[s]:
                meta[t] = ConfigLoader(t)
        with open(path, 'wb') as f:
            pickle.dump(meta, f)
    return meta


arbc = Resolver()


if __name__ == "__main__":
    sys.exit(main())
