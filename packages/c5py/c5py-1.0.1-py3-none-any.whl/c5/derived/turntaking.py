from c5.config import arbc, SAMPLING_INTERVAL

import numpy as np
import pandas as pd

TURNTRANSITION_DT = np.dtype({'names': ['start', 'end', 'type', 'length_before', 'length', 'length_after'],
                              'formats': ['u8', 'u8', 'u8', 'u8', 'u8', 'u8']})
TURNS_PATH = arbc.stage2.turns()


def generate_turns(db):
    seq = {}
    for trial in db.keys():
        seq[int(trial[-3:])] = extract_turntaking(db[trial])
    return seq


def extract_turntaking(data):
    tmp = np.zeros(data.shape[0], dtype=[('timestamp', 'u8'), ('speech', 'i4')])
    tmp['timestamp'] = data['timestamp']
    tmp['speech'] = data['speech1'] + 2 * data['speech2']
    current = tmp[0]
    seq = []
    for x in tmp:
        if x['speech'] != current['speech']:
            # treat *exact* turn transition as a very small pause; these cases are rare!
            if x['speech'] in [1, 2] and current['speech'] in [1, 2]:
                x_buffer = dict(timestamp=x['timestamp']-SAMPLING_INTERVAL/2, speech=0)
                seq.append((current['timestamp'], x_buffer['timestamp'], current['speech'],
                            0, x_buffer['timestamp'] - current['timestamp'], 0))
                current = x_buffer
            seq.append((current['timestamp'], x['timestamp'], current['speech'],
                        0, x['timestamp']-current['timestamp'], 0))
            current = x
    x = tmp[-1]
    seq.append((current['timestamp'], x['timestamp'], current['speech'],
                0, x['timestamp']-current['timestamp'], 0))
    arr = np.array(seq, dtype=TURNTRANSITION_DT)
    return classify_turntaking(arr)


def classify_turntaking(seq):
    classed_seq = np.copy(seq)
    classed_seq[0]["length_after"] = classed_seq[1]["length"]
    for idx in range(len(seq)-2):
        classed_seq[idx+1]["length_before"] = seq[idx]["length"]
        classed_seq[idx+1]["type"] = str(seq[idx]["type"])+str(seq[idx+1]["type"])+str(seq[idx+2]["type"])
        classed_seq[idx+1]["length_after"] = seq[idx+2]["length"]
    classed_seq[-1]["length_before"] = seq[-2]["length"]
    return classed_seq


def filter_turntaking_types(seqf, types, length):
    if not isinstance(seqf, pd.DataFrame):
        seqf = pd.DataFrame(seqf)
    res = seqf[seqf.type.isin(types)]
    res = res[(res.length_before >= length) & (res.length_after >= length)]
    return res
