# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:38:03 2014

@author: alneuman
"""

import os.path
import sys
import struct
import numpy as np
import pandas as pd
import c5.config
from c5.config import TRIALS, RAW_PATH, STAGE1_PATH
import c5.data
import c5.sensors
import os
import tempfile
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def check(path, trial):
    cfg = os.path.exists("%s/trial%d.json" % (path, trial))
    b1 = os.path.exists("%s/trial%d_brix_s1.log" % (path, trial))
    b2 = os.path.exists("%s/trial%d_brix_s2.log" % (path, trial))
    return (cfg and b1 and b2)


def load_brix_log(filename):
    tmp_fd, tmp_path = tempfile.mkstemp()
    with os.fdopen(tmp_fd, 'w') as tmp_file:
        with open(filename, 'r') as f:
            for line in f:
                l = line.replace(':', ',')
                v_arr = l.split(',')
                if len(v_arr) == 7:
                    tmp_file.write(l)
                elif len(v_arr) == 13:
                    try:
                        tmp = []
                        for i in range(6):
                            msb = int(v_arr[(i*2)+1])
                            lsb = int(v_arr[(i*2)+2])
                            c = struct.pack("B", msb) + struct.pack("B", lsb)
                            tmp.append(struct.unpack(">h", c)[0])
                        tmp_file.write("%s,%d,%d,%d,%d,%d,%d\n" %
                                       (v_arr[0], tmp[0], tmp[1], tmp[2],
                                        tmp[3], tmp[4], tmp[5]))
                    except ValueError:
                        logger.info("dropped line %s", v_arr)
                else:
                    logger.info("dropped line %s", v_arr)
    result = np.loadtxt(tmp_path, skiprows=1, delimiter=',',
                        dtype=c5.config.BRIX_DT)
    os.remove(tmp_path)
    return result


def _benchmark_check(path, trial):
    out1 = os.path.exists("%s/brix_outlier1.log" % (path, trial))
    out2 = os.path.exists("%s/brix_outlier2.log" % (path, trial))
    return (check(path, trial) and out1 and out2)


def convert_data(path, trial, out=None):
    if out is not None:
        out1_path = "%s/trial%d_brix_s1.csv" % (out, trial)
        out2_path = "%s/trial%d_brix_s2.csv" % (out, trial)
        if os.path.exists(out1_path) or os.path.exists(out2_path):
            print("Data for trial %d already exist. skip" % trial)
            return

    # load brix data: already removes incomplete lines
    b1 = load_brix_log("%s/trial%d_brix_s1.log" % (path, trial))
    b2 = load_brix_log("%s/trial%d_brix_s2.log" % (path, trial))

    # brix got unix timestamps; no fix required
    # detect outlier for AR-Baseline and Face-to-Face
    if trial // 100 < 3:
        o1 = detect_outlier(b1)
        o2 = detect_outlier(b2)
        b1 = np.delete(b1, o1)
        b2 = np.delete(b2, o2)

    # rescale returns pd.DataFrame
    b1_new = rescale_signal(b1)
    b2_new = rescale_signal(b2)

    # adapt header to standard numpy format
    head = list(c5.config.BRIX_DT.names)
    head[0] = "# " + head[0]

    if out is not None:
        b1_new.to_csv(out1_path, index=False, header=head, float_format='%.3f')
        b2_new.to_csv(out2_path, index=False, header=head, float_format='%.3f')
    else:
        return b1_new, b2_new


def int2bit(value):
    # little endian short expected
    func = struct.Struct('<h').pack
    lsb, msb = func(value)
    return lsb, msb


def detect_outlier(data, sensors=None, params=None):
    out = []
    if sensors is None:
        sensors = c5.config.BRIX_DT.names
    for key in sensors:
        if key == 'timestamp':
            continue
        arr = [int2bit(x) for x in data[key]]
        arr = np.array(arr)
        out_tmp = _detect_outlier_step(arr, params)
        out.extend(out_tmp)
    dt = data['timestamp'][1:] - data['timestamp'][:-1]
    out = np.unique(out)

    # condition 3: if too much time passed between two samples, remove marker
    res = []
    dt = np.where(dt > 200)[0]
    for idx in out:
        #print dt
        #print idx
        if (idx-1) not in dt:
            res.append(idx)
    return res


def _detect_outlier_step(data, params):
    if params is None:
        # retrieved by test run see Pre-Brix notebook
        params = {'msb_lag': 48, 'lsb_shift': 198, 'lsb_lag': 61}
    # we check two conditions
    out1 = np.zeros(data.shape[0])
    out2 = np.zeros(data.shape[0])
    t_lsb = data[0, 0]
    t_hsb = data[0, 1]
    for i in range(0, data.shape[0]):
        c_lsb = data[i, 0]
        c_hsb = data[i, 1]

        abs_lsb = abs(t_lsb - c_lsb)
        abs_hsb = abs(t_hsb - c_hsb)
        # 1st condition: if there is a lsb drop without any msb activity,
        # we assume ansynchronous reading
        if abs_hsb == 0:
            if abs_lsb > params['lsb_shift']:
                # to avoid double detection we only classify if
                # the preceeding frame wasnt classified
                if out1[i-1] + out2[i-1] == 0:
                    out1[i] = 1
        # 2nd condition: if there is change in the msb but almost none in lsb
        else:
            # 2a: msb shift indicates change of signs
            if abs_hsb > 128:
                if abs_lsb < params['lsb_lag']:
                    if out1[i-1] + out2[i-1] == 0:
                        out2[i] = 1
            # 2b: msb indicates significant value change
            else:
                if abs_lsb < params['msb_lag']:
                    if out1[i-1] + out2[i-1] == 0:
                        out2[i] = 1
        t_hsb = c_hsb
        t_lsb = c_lsb
    out = []
    # summarize outliers
    for i in range(0, data.shape[0]):
        if out1[i] + out2[i] > 0:
            out.append(i)
    return out


# gyro is 14.375 LSB/ deg/s and acc is 256 LSB/g
def rescale_signal(data):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    gyro = data.filter(regex="gyro").apply(lambda x: x / 14.375)
    converted = pd.concat([data.filter(regex="time"),
                           gyro.subtract(gyro.mean()),
                           data.filter(regex="acc").apply(lambda x: x / 256.0)],
                          axis=1).reindex(data.index)
    return converted


def main():
    for study, trials in TRIALS.items():
        for trial in trials:
            raw = "%s/%s/trial%d" % (RAW_PATH, study, trial)
            vol = "%s/%s/trial%d" % (STAGE1_PATH, study, trial)
            if check(raw, trial) is False:
                print("data missing. exit")
                return
            convert_data(raw, trial, vol)


if __name__ == "__main__":
    sys.exit(main())
