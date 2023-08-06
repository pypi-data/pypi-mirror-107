from c5.config import FILE_NAMES, STAGE1_PATH, STUDIES, STUDIES_ACRONYMS, TRIALS
from c5.config import INERTIAL_DT, get_config
from c5.data import create_slots
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def collect_orientation_data():
    db = {}
    for study, trials in TRIALS.items():
        for trial in trials:
            b1, b2 = get_brix_data(trial)
            db[trial] = (b1, b2)
    return db


def get_brix_data(tid):
    fb1 = FILE_NAMES['brix_s1'].format(tid=tid)
    fb2 = FILE_NAMES['brix_s2'].format(tid=tid)

    f = "%s/%s/trial%d/%s" % (STAGE1_PATH, STUDIES[STUDIES_ACRONYMS[tid // 100 - 1]], tid, fb1)
    b1 = np.loadtxt(f, dtype=INERTIAL_DT, delimiter=',')
    f = "%s/%s/trial%d/%s" % (STAGE1_PATH, STUDIES[STUDIES_ACRONYMS[tid // 100 - 1]], tid, fb2)
    b2 = np.loadtxt(f, dtype=INERTIAL_DT, delimiter=',')

    con, tid = get_config(b1['timestamp'][0])
    start = con.get('trial.phase.negotiation.start')
    stop = con.get('trial.phase.negotiation.stop')
    trial_start = con.get('trial.start')

    b1 = create_slots(b1, start, stop).pad().fillna(method='bfill').dropna()
    b1['trial_time'] = b1.timestamp - trial_start
    b2 = create_slots(b2, start, stop).pad().fillna(method='bfill').dropna()
    b2['trial_time'] = b2.timestamp - trial_start
    if b1.shape != b2.shape:
        raise ValueError("Inertial data have differing length!")
    return b1, b2
