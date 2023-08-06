import io
import nbformat

from IPython.display import display, Image, Markdown, HTML, clear_output
from IPython.lib.deepreload import reload as dreload
from IPython import get_ipython

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as pl
import numpy as np
import seaborn as sns
import os

import c5.output
import c5.sensors
import c5.derived
from c5.config import arbc, SAMPLING_INTERVAL, SAMPLING_RATE, SYNC_XML, MARKER_NAMES
from c5.config import TRIALS, STUDIES_ACRONYMS, MARKER_ACRONYMS, TRIAL_IDS, ACRONYM_IDS, MARKER_IDS
from c5.data import stage2_cached
from scipy.stats import ks_2samp, ttest_ind, describe
import scipy.signal
import logging
import sys

colors = sns.color_palette()

# pl.style.use('dark_background')
# mpl.rcParams['font.family'] = 'sans-serif'
# mpl.rcParams['font.sans-serif'] = ['Repro'] + mpl.rcParams['font.sans-serif']
# bg_color = 'navy'
# mpl.rcParams.update({'axes.facecolor':bg_color, 'figure.facecolor': bg_color, 'savefig.facecolor': bg_color})
# colors = sns.color_palette("pastel")

class ProgressContext:

    DEFAULT_TEXT = "Progress: [{0}] {1:.1f}%"
    DEFAULT_SYMBOL = "#"

    def __init__(self, min_val=0, max_val=1, bar_length=20, text=None):
        self.min_val = min_val
        self.max_val = max_val
        self.bar_length = bar_length
        self._progress = 0
        self.text = self.DEFAULT_TEXT if text is None else text

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = min(1, max(value, 0))
        self._update_output()

    def update(self, value):
        self.progress = value

    def _update_output(self):
        bl = self.bar_length
        p = self.progress
        block = int(round(bl * p))
        clear_output(wait=True)
        print(self.text.format(self.DEFAULT_SYMBOL * block + "-" * (bl - block), p * 100))

    def __enter__(self):
        self.update(0)
        return self

    def __exit__(self, *args):
        clear_output(wait=False)


# decorator
def with_progress(func):

    def decorator_func(*args, **kwargs):
        try:
            with ProgressContext() as p:
                progress_kwargs = dict(progress_callback=p.update)
                progress_kwargs.update(kwargs)
                return func(*args, **progress_kwargs)
        except TypeError:
            return func(*args, **kwargs)
    return decorator_func


def execute_notebook(nbfile):
    with io.open(nbfile, encoding='utf-8') as f:
        nb = nbformat.read(f, nbformat.current_nbformat)
    ip = get_ipython()
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        ip.run_cell(cell.source)


def update_figure_size(x=16, y=4, fdpi=150, sdpi=150):
    mpl.rcParams['figure.dpi'] = fdpi
    mpl.rcParams['savefig.dpi'] = sdpi
    mpl.rcParams['figure.figsize'] = (x, y)


def _interact(*args, **kwargs):
    def real_decorator(func):
        func()
        return None
    return real_decorator


env_interactive = os.environ["C5_NB_INTERACTIVE"] if "C5_NB_INTERACTIVE" in os.environ else "True"
interactive = env_interactive not in ["False", "0", "false"]

# If session is interactive import interact from ipywidgets
if interactive:
    from ipywidgets import interact
else:
    # otherwise import function caller decorator
    interact = _interact

env_debug = os.environ["DEBUG"] if "DEBUG" in os.environ else "True"
debug = env_debug in ["True", "1", "true"]

if debug:
    logger = logging.getLogger('c5')
    handler = logging.StreamHandler(os.fdopen(1, "w"))
    handler.setFormatter(
        logging.Formatter("[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s] %(message)s", "%H:%M:%S"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
