# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from six import string_types
import threading
import c5.config
from os.path import splitext, join, exists
from os import remove, environ
import pickle
from scipy.stats import kstwobign, pearsonr
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())


# Wraps pandas pickle and h5 storage into a convenient transparent container
class DataStorage(object):

    def __init__(self, file_path, read_only=True, insert=None):
        insert = {} if insert is None or read_only is True else insert
        self.file_path = file_path
        self.read_only = read_only
        self._init_container()
        if not isinstance(insert, dict):
            raise AttributeError("insert seed should be of type 'dict' but is " + str(type(insert)))
        for k, v in insert.items():
            self[k] = v

    def _init_container(self):
        _, ext = splitext(self.file_path)
        if ext == ".pkl":
            if not exists(self.file_path):
                self.container = {}
                self.save()
            else:
                with open(self.file_path, 'rb') as f:
                    self.container = pickle.load(f)
        elif ext == ".h5":
            self.container = pd.HDFStore(self.file_path, mode='r' if self.read_only else 'a')
        else:
            raise AttributeError("Extension '{0}' not known!".format(ext))

    def fix_timestamp_freq(self):
        """Fixes frequency related pandas issues when 'Expected unicode, got pandas._libs.properties.CachedProperty' occurs."""
        _, ext = splitext(self.file_path)
        if ext == ".h5":
            self.container.close()
            self.container = pd.HDFStore(self.file_path, mode='a')
            for key in self.container.keys():
                value = self.container[key]
                if isinstance(value, pd.DataFrame) and hasattr(value.index, 'freq') and not isinstance(value.index.freq.freqstr, string_types):
                    value.index.freq = "{0}{1}".format(value.index.freq.n, value.index.freq.rule_code)
                    self.container[key] = value
            self.save(close=True)
            self.container = pd.HDFStore(self.file_path, mode='r' if self.read_only else 'a')


    def save(self, close=False):
        # HDFStores are written back to disk instantly
        if not isinstance(self.container, pd.HDFStore):
            with open(self.file_path, 'wb') as f:
                pickle.dump(self.container, f)
        elif close:
            self.container.close()

    def keys(self):
        return self.container.keys()

    def items(self):
        return self.container.items()

    def __getitem__(self, key):
        if isinstance(self.container, pd.HDFStore) and isinstance(key, int):
            key = "/trial{0}".format(key)
        return self.container[key]

    def __setitem__(self, key, value):
        if self.read_only:
            raise ValueError("DataStorage is set to read-only!")
        if isinstance(self.container, pd.HDFStore) and isinstance(key, int):
            key = "/trial{0}".format(key)
        self.container[key] = value
        self.save()

    def __iter__(self):
        return self.container.__iter__()

    def __next__(self):
        return self.container.__next__()

    def __contains__(self, key):
        if isinstance(self.container, pd.HDFStore) and isinstance(key, int):
            key = "/trial{0}".format(key)
        return self.container.__contains__(key)


# decorator
def stage2_cached(file_name, read_only=True, override=None):
    override = environ.get('DISABLE_CACHE', 'false').lower() in ['1', 'true', 'on'] if override is None \
                                                                                    else override
    if callable(file_name):
        file_name = file_name()
    if not file_name.startswith(c5.config.arbc.stage2()):
        file_name = join(c5.config.arbc.stage2(), file_name)

    def decorator(func):
        cache = dict(path=file_name, read_only=read_only, override=override)

        def decorator_func(*args, **kwargs):
            if not exists(cache['path']) or cache['override']:
                _LOGGER.info("Could not find cached version of %s or override is requested. Calling passed function.",
                             cache['path'])
                data = func(*args, **kwargs)
                # remove old only after new data has been generated in case
                # override is executed accidentally
                if exists(cache['path']):
                    remove(cache['path'])
                ds = DataStorage(cache['path'], read_only=False, insert=data)
                ds.save(close=True)
            _LOGGER.info("Accessing data stored in %s.", cache['path'])
            return DataStorage(cache['path'], read_only=cache['read_only'])
        return decorator_func

    return decorator


def create_slots(data, start=None, stop=None, frame=c5.config.SAMPLING_INTERVAL):
    if data.shape[0] == 0:
        if start is None or stop is None:
            raise ValueError("Passed data is empty")
        else:
            _LOGGER.warning("Passed data is empty. Since start and stop are given, an NaN set will be returned.")
            data = pd.DataFrame(data).reindex([start, stop])
            data['timestamp'] = data.index
    elif isinstance(data, np.ndarray) and not isinstance(data[0], np.void):
        raise AssertionError("row type is %s but numpy void is required" % type(data[0]))
    data = pd.DataFrame(data)
    start = start if start is not None else data.timestamp.iloc[0]
    stop = stop if stop is not None else data.timestamp.iloc[data.shape[0]-1]
    period = data[(data.timestamp >= start) & (data.timestamp <= stop)]
    tmp = pd.DataFrame(period).set_index('timestamp', drop=False)
    ts = tmp.index
    if len(ts) < 1 or ts[0] != start:
        ts = ts.insert(0, start)
    if len(ts) < 2 or ts[-1] != stop:
        ts = ts.insert(len(ts), stop)
    tmp = tmp.reindex(ts)
    tmp['datetime'] = pd.to_datetime(tmp.index, unit='ms')
    tmp.set_index('datetime', inplace=True)
    tmp = tmp.resample('%dL' % frame, label='right')
    return tmp


def sliding_window(data, func, window, stepsize=1):
    res = [0] * (window//stepsize)
    for idx in range(window, data.shape[0], stepsize):
        res.append(func(data[idx-window:idx]))
    return res


def weight_decay(x, last=0, b=0.95):
    c1 = (last + x) * b
    return c1


def window_sum(x, window, overlap=1):
    result = np.zeros(x.shape[0])
    window = int(window)
    for idx in range(window,x.shape[0]):
        result[idx] = x[idx-window:idx].sum()
    return result


def dict_to_array(db):
    res = []

    for tid in db.keys():
        tmp = db[tid] if isinstance(db[tid], pd.DataFrame) else pd.DataFrame(db[tid])
        tid = int(tid[-3:]) if isinstance(tid, string_types) else tid
        if hasattr(tmp.index, 'freq') and not isinstance(tmp.index.freq.freqstr, string_types):
            tmp.index.freq = "{0}{1}".format(tmp.index.freq.n, tmp.index.freq.rule_code)
        tmp = tmp.assign(tid=tid)
        res.append(tmp)
    return pd.concat(res)


def frames_to_sequences(data, timestamps=None, dtype=None):
    # if data is a pandas Series, we can use the shift/group approach and ignore timestamp
    if isinstance(data, pd.Series) and isinstance(data.index, pd.DatetimeIndex):
        return _frames_to_sequences(data)
    stacked = np.vstack((timestamps, data)).transpose()
    last = stacked[0]
    res = []
    for s in stacked:
        if last[1] != s[1]:
            res.append((last[1], last[0], s[0], s[0]-last[0]))
            last = s
    s = stacked[-1]
    res.append((last[1], last[0], s[0], s[0]-last[0]))
    return np.array(res, dtype=[('data', dtype), ('start', 'u8'), ('end', 'u8'), ('duration', 'u8')])


def _frames_to_sequences(frames):
    delta = (frames.index[1] - frames.index[0]) // np.timedelta64(1, 'ms')
    grouper = (frames != frames.shift(1)).cumsum()
    durs = frames.groupby(grouper).transform('size')
    durs = durs[grouper.shift() != grouper]
    seqs = frames[durs.index].copy().to_frame()
    seqs['duration'] = durs * delta
    try:
        start = frames.timestamp
    except AttributeError:
        start = seqs.index
    seqs['start'] = c5.data.datetime_to_unixtime(start)
    seqs['stop'] = seqs.start + seqs.duration
    return seqs.sort_values(by='start').reset_index(drop=True)


def sequences_to_frames(data, sampling=c5.config.SAMPLING_INTERVAL, **kwargs):
    tmp = pd.DataFrame(data).copy()
    tmp['datetime'] = pd.to_datetime(tmp.timestamp, unit='ms')
    tmp.set_index('datetime', inplace=True)
    # add new entry to have the last sequence included as well
    tmp.loc[pd.to_datetime(tmp.index.asi8[-1] + tmp.duration[-1] * 1e6)] = np.NaN
    tmp = tmp.resample('%dL' % sampling, **kwargs).pad()
    t = (tmp.timestamp + tmp.duration) * 1e6 < tmp.index.asi8
    tmp[t] = np.NaN
    return tmp


def flatten(data):
    return list(sum(data, ()))


def mollifier(size, e=1):
    result = []
    for x in np.arange(-e, e, 2 * e / float(size)):
        j = 1/e**2 * np.exp(-1/(1 - (x/e)**2))
        result.append(j)
    return np.array(result)


def norm_value_range(data):
    mn = np.min(data)
    mx = np.max(data)
    data -= mn
    if mx == mn:
        return
    data /= (mx-mn)


def resample(data, size):
    step = data.shape[0] / float(size)
    x = np.arange(start=0, stop=data.shape[0], step=step)
    xp = np.arange(data.shape[0])
    res = np.interp(x, xp, data)
    return res


def summarize(data, size):
    res = np.zeros(size)
    step = data.shape[0] / float(size)
    for idx, i in enumerate(np.arange(step, data.shape[0], step)):
        res[idx] = data[int(i-step):int(i)].sum()
    return res


def get_phase(data, trial=None, phase='negotiation', timestamps=None, meta=None):
    tmp = {trial: data} if trial is not None else data

    for tid, data in tmp.items():
        timestamps = timestamps if timestamps is not None else data['timestamp']

        if timestamps.shape[0] != data.shape[0]:
            raise ValueError('Dimension mismatch! Data dimension is %d but timestamps is %d' %
                             (data.shape[0], timestamps.shape[0]))

        if isinstance(phase, str):
            con = c5.config.ConfigLoader(tid) if meta is None else meta[tid]
            phase_start = con.get("trial.phase.%s.start" % phase)
            phase_stop = con.get("trial.phase.%s.stop" % phase)
        else:
            phase_start, phase_stop = phase

        filtered_before = timestamps > phase_start
        data = data[filtered_before]
        if timestamps.shape[0] != data.shape[0]:
            timestamps = timestamps[filtered_before]
        data = data[timestamps < phase_stop]
        tmp[tid] = data
    return tmp[trial] if trial is not None else tmp


def unix_to_trial_time(data, key='trial.start'):
    ts = data['timestamp'][0]
    conf = c5.config.get_config(ts)
    data['timestamp'] - conf.get(key)


# http://stackoverflow.com/a/32853294/1617563
def fill_gaps(data, value, cond, maxgap):
    # increase condition counter whenever condition is NOT met consecutively
    grouper = (cond != cond.shift(1)).cumsum() * cond
    # creates a grouper like 0,1,1,2,3,4,4..., where same number means same group
    # and therefore an area where the condition is met
    fill = (data.groupby(grouper).transform('size') <= maxgap)
    res = data.copy()
    res.loc[fill] = value
    return res


# based on https://gist.github.com/fccoelho/301518
def peak_detection(data, delta):
    maxtab = []
    mintab = []
    x = np.arange(data.shape[0])
    mn, mx = np.Inf, -np.Inf
    mnpos = mxpos = np.NaN
    lookformax = True

    for i in x:
        this = data[i]
        if this > mx:
            mx = this
            mxpos = i
        if this < mn:
            mn = this
            mnpos = i

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = i
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = i
                lookformax = True
    return np.array(maxtab, dtype=object), np.array(mintab, dtype=object)


# https://stackoverflow.com/a/37616966/1617563
# Create models from data
def fit_distributions(data, distributions=None):
    """Model data by finding best fit distribution to data"""

    import scipy.stats as st
    import warnings

    # Distributions to check
    distributions = [
        st.alpha, st.anglit, st.arcsine, st.beta, st.betaprime, st.bradford, st.burr, st.cauchy,
        st.chi, st.chi2, st.cosine, st.dgamma, st.dweibull, st.erlang, st.expon, st.exponnorm,
        st.exponweib, st.exponpow, st.f, st.fatiguelife, st.fisk, st.foldcauchy, st.foldnorm,
        st.genlogistic, st.genpareto, st.gennorm, st.genexpon, st.genextreme,
        st.gamma, st.gengamma, st.genhalflogistic, st.gilbrat, st.gompertz, st.gumbel_r, st.gumbel_l, st.halfcauchy,
        st.halflogistic, st.halfnorm, st.halfgennorm, st.hypsecant, st.invgamma, st.invgauss, st.invweibull,
        st.johnsonsb, st.johnsonsu, st.ksone, st.kstwobign, st.laplace, st.levy, st.levy_l, st.logistic,
        st.loggamma, st.loglaplace, st.lognorm, st.lomax, st.maxwell, st.mielke, st.nakagami, st.ncx2, st.ncf, st.nct,
        st.norm, st.pareto, st.pearson3, st.powerlaw, st.powerlognorm, st.powernorm, st.rdist, st.reciprocal,
        st.rayleigh, st.rice, st.recipinvgauss, st.semicircular, st.t, st.triang, st.truncexpon, st.truncnorm,
        st.tukeylambda, st.uniform, st.vonmises_line, st.wald, st.weibull_min, st.weibull_max,
        st.wrapcauchy
    ] if distributions is None else [getattr(st, d) for d in distributions]

    # Best holders
    best_distribution = st.norm
    bics = []
    fitting_params = {best_distribution.name: (0.0, 1.0)}

    # Estimate distribution parameters from data
    for distribution in distributions:
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Calculate fitted PDF and negative log Likelihood
                d_bic, d_nll = bic(data, distribution, *params)
                bics.append((distribution.name, d_bic, d_nll))
                fitting_params[distribution.name] = params

        except Exception as e:
            print(e)
            pass

    errors = pd.DataFrame(bics, columns=['distribution', 'bic', 'nll']).sort_values(by='bic')
    return fitting_params, errors


# Bayesian information criterion
# BIC = ln(n)*k - 2ln(L)
def bic(data, distribution, *args):
    nll = -np.sum(distribution.logpdf(data, *args), axis=0)
    return np.log(data.shape[0]) * len(args) + 2 * nll, nll


def datetime_to_unixtime(datetime):
    try:
        return datetime.asi8 // 1e6
    except AttributeError:
        return datetime.asm8.astype('uint64') // 1e6


# https://github.com/syrte/ndtest/blob/master/ndtest.py
def ks2d2s(x1, y1, x2, y2, nboot=None, extra=False):
    assert (len(x1) == len(y1)) and (len(x2) == len(y2))
    n1, n2 = len(x1), len(x2)
    D = _avgmaxdist(x1, y1, x2, y2)

    if nboot is None:
        sqen = np.sqrt(n1 * n2 / (n1 + n2))
        r1 = pearsonr(x1, y1)[0]
        r2 = pearsonr(x2, y2)[0]
        r = np.sqrt(1 - 0.5 * (r1 ** 2 + r2 ** 2))
        d = D * sqen / (1 + r * (0.25 - 0.75 / sqen))
        p = kstwobign.sf(d)
    else:
        n = n1 + n2
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        d = np.empty(nboot, 'f')
        for i in range(nboot):
            idx = np.random.choice(n, n, replace=True)
            ix1, ix2 = idx[:n1], idx[n1:]
            # ix1 = random.choice(n, n1, replace=True)
            # ix2 = random.choice(n, n2, replace=True)
            d[i] = _avgmaxdist(x[ix1], y[ix1], x[ix2], y[ix2])
        p = np.sum(d > D).astype('f') / nboot
    if extra:
        return p, D
    else:
        return p


def _avgmaxdist(x1, y1, x2, y2):
    D1 = _maxdist(x1, y1, x2, y2)
    D2 = _maxdist(x2, y2, x1, y1)
    return (D1 + D2) / 2


def _maxdist(x1, y1, x2, y2):
    n1 = len(x1)
    D1 = np.empty((n1, 4))
    for i in range(n1):
        a1, b1, c1, d1 = _quadct(x1.iloc[i], y1.iloc[i], x1, y1)
        a2, b2, c2, d2 = _quadct(x1.iloc[i], y1.iloc[i], x2, y2)
        D1[i] = [a1 - a2, b1 - b2, c1 - c2, d1 - d2]

    # re-assign the point to maximize difference,
    # the discrepancy is significant for N < ~50
    D1[:, 0] -= 1 / n1

    dmin, dmax = -D1.min(), D1.max() + 1 / n1
    return max(dmin, dmax)


def _quadct(x, y, xx, yy):
    n = len(xx)
    ix1, ix2 = xx <= x, yy <= y
    a = np.sum(ix1 & ix2) / n
    b = np.sum(ix1 & ~ix2) / n
    c = np.sum(~ix1 & ix2) / n
    d = 1 - a - b - c
    return a, b, c, d


class WorkerThread(threading.Thread):
    def __init__(self, func, *args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.done = False

    def run(self):
        self.func(*self.args)
        self.done = True
        print("done")

    def is_done(self):
        return self.done
