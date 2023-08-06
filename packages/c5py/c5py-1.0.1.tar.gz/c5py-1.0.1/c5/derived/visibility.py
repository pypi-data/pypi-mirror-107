import c5.config
import pandas as pd
import numpy as np
import logging

from six import string_types

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

VISIBILITY_PATH = c5.config.STAGE2_PATH + "/" + c5.config.STAGE2_NAMES['object_visibility']


DU_X_MM = 400
DU_Y_MM = 800


def generate_visual_attention(marker_data, threshold=1000):
    visibility = {}
    for tid in marker_data:
        logger.info('Processing %s', tid)
        visibility[tid] = get_visual_attention(marker_data[tid], threshold)
    return visibility


def get_visual_attention(data, thresh):
    data = data.copy()
    data["timestamp"] = data.index.asi8 // 1e6
    vis = {}
    for mid in c5.config.MARKER_IDS:
        cols = ["visible_m%d_hmd1" % mid, "visible_m%d_hmd2" % mid]
        tmp = pd.DataFrame(index=data.index, columns=cols)
        tmp = tmp.fillna(0)
        for hmd in ['hmd1', 'hmd2']:
            s_x = 's_x_m%d_%s' % (mid, hmd)
            s_y = 's_y_m%d_%s' % (mid, hmd)
            delta = 'delta_m%d_%s' % (mid, hmd)
            visible = 'visible_m%d_%s' % (mid, hmd)
            try:
                data.loc[(data[delta] > thresh), [s_x, s_y]] = np.nan
                x = (data[[s_x, s_y]] - 0.5).abs()
                tmp.loc[data[s_x] > 0, visible] = 0.5
                tmp.loc[(x[s_x] < 0.25) & (x[s_y] < 0.25), visible] += 0.4
            except KeyError:
                logger.warn("No %d in for %s in trial" % (mid, hmd))
        vis[mid] = tmp
    cols = [data.timestamp]
    cols.extend(vis.values())
    return pd.concat(cols, axis=1)


def position_to_velocity(data, jitter=0.1, max_delta=40):
    df = data.copy()
    travel = {}
    for mid in c5.config.MARKER_ACRONYMS.keys():
        try:
            delta = 'delta_m%d_cam3' % mid
            sx = 's_x_m%d_cam3' % mid
            sy = 's_y_m%d_cam3' % mid
            tmp = df[[sx, sy]].copy()
            m_pos = tmp[df[delta] <= max_delta]
            timestamps = pd.Series(tmp.index.asi8 // 1e6, index=tmp.index)

            # derive velocity absolute velocity data from position
            # convert display units into velocity and display units into mm
            velo_xy = m_pos.diff().abs() * [DU_X_MM, DU_Y_MM]
            # calculate resulting velocity from x and y components
            velo = (velo_xy[sx] ** 2 + velo_xy[sy] ** 2).apply(np.sqrt)
            # remove jitter
            velo[velo < jitter] = 0
            # convert values into mm/ms
            velo /= timestamps[m_pos.index].diff()
            travel[mid] = pd.DataFrame({'timestamp': timestamps, 'velocity': velo}, index=tmp.index)
            travel[mid].velocity.fillna(method='bfill', inplace=True)
        except KeyError:
            travel[mid] = pd.DataFrame([[0, 0]], columns=['timestamp', 'velocity'])
    return travel


def most_moved(travel):
    max_velo = travel[111].copy()
    if hasattr(max_velo.index, 'freq') and not isinstance(max_velo.index.freq.freqstr, string_types):
        max_velo.index.freq = "{0}{1}".format(max_velo.index.freq.n, max_velo.index.freq.rule_code)
    max_velo['mid'] = 0
    for mid, m in travel.items():
        try:
            c = max_velo.velocity < m.velocity
            max_velo.loc[c, 'velocity'] = m.loc[c, 'velocity']
            max_velo.loc[c, 'mid'] = mid
        except:
            pass
    return max_velo
