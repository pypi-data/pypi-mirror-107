# -*- coding: utf-8 -*-

import subprocess

import numpy as np
from scipy import signal
import matplotlib.pylab as pl
import seaborn as sn
from collections import OrderedDict

from matplotlib.ticker import AutoLocator, FuncFormatter, MultipleLocator
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection
from matplotlib.colorbar import ColorbarBase

import c5.data


class SelectXRange:
    def __init__(self, fig, f):
        self.fig = fig
        self.func = f
        self.click = fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.release = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.a = None
        self.pos = None
        #self.press = fig.canvas.mpl_connect('key_release_event', self.on_press)
        #self.draw = fig.canvas.mpl_connect('draw_event', self.on_draw)

    def on_click(self, event):
        if event.button != 1: return
        if pl.get_current_fig_manager().toolbar.mode != '': return
        self.a = event.xdata
        self.pos = event.x

    def on_release(self, event):
        if (event.button != 1) or (self.a is None) : return
        if abs(self.pos - event.x) < 10: return
        self.func(min(self.a,event.xdata),max(self.a,event.xdata))
        self.a = None
        self.pos = None


class _PlotPlayer:
    def __init__(self, data, filename, offset):
        self.timestamps = data[:]['timestamp']
        self.ydata = []
        for i in data.dtype.names:
            if i == 'timestamp': continue
            if i == 'delta': continue
            self.ydata.append(data[:][i])
        self.duration = self.timestamps[-1] - self.timestamps[0]
        self.duration /= 1000.0
        self.start = (self.timestamps[0]-offset)/1000.0
        if ".wav" in filename:
            f = scikits.audiolab.Sndfile(filename,'r')
            skips =  self.start * f.samplerate
            skips = int(skips)
            while (skips > 0):
                read = min(100000,skips)
                f.read_frames(read)
                skips -= read
            self.sample = f.read_frames(int(self.duration * f.samplerate)).transpose()
            f.close()
        else: self.sample = None
        self.call = ['mplayer','-ss',str(self.start),'-endpos',str(self.duration),filename]

    def show(self):
        sets = len(self.ydata)
        self.fig = pl.figure()
        if self.sample is not None:
            ax = self.fig.add_subplot(sets+2,1,1)
            d1 = c5.data.resample(self.sample[0,:], self.timestamps.shape[0])
            ax.plot(self.timestamps, np.abs(d1))
            if self.sample.shape[1] > 1:
                d2 = c5.data.resample(self.sample[1,:], self.timestamps.shape[0])
                ax.plot(self.timestamps, np.abs(d2)*-1)
                ax.set_xlim(self.timestamps[0],self.timestamps[-1])
        for i in range(sets+1):
            ax = self.fig.add_subplot(sets+2,1,i+2)
            ax.set_xlim(self.timestamps[0],self.timestamps[-1])
            if i < sets:
                ax.plot(self.timestamps, self.ydata[i])
            else:
                ax = self.fig.add_subplot(sets+2,1,i+2)
                self.bplay = Button(ax, 'Play')
                self.bplay.on_clicked(self.play)
        self.fig.show()

    def play(self, event):
        print(self.call)
        self.thread = c5.data.WorkerThread(subprocess.call,self.call)
        self.thread.start()


class PlotPlayer:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
    def show_range(self, x, y):
        d = self.data[(self.data[:]['timestamp'] >= x) & (self.data[:]['timestamp'] <= y)]
        player = _PlotPlayer(d, self.filename,self.data[0]['timestamp'])
        player.show()


def _minute_formatter_seconds(x, pos):
    return _minute_formatter(x*1000, pos)


def _minute_formatter(x, pos):
    # just returns minutes
    return '%02d:%02d' % ((x % 3600000) / 60000, (x % 60000) / 1000.0)


def _unix_formatter(x, pos):
    return '%02d:%02d:%02d' % ((x % 8.64e+7) / 3600000, (x % 3600000) / 60000, (x % 60000) / 1000.0)


def format_time(ax=None, ticks=None, rotation=None):
    if ax is None:
        ax = pl.gca().get_xaxis()
    if ticks is None:
        majorLocator = AutoLocator()
    else:
        majorLocator = MultipleLocator(ticks)

    t = ax.get_data_interval()[1]
    # no experiment should be longer than 2700 seconds (45 * 60)
    if t < 2700:
        time_formatter = _minute_formatter_seconds
    # a value bigger than this indicates unix time in ms
    elif t < 1e12:
        time_formatter = _minute_formatter
    else:
        time_formatter = _unix_formatter
    majorFormatter = FuncFormatter(time_formatter)
    ax.set_major_locator(majorLocator)
    ax.set_major_formatter(majorFormatter)
    if rotation:
        for label in ax.get_ticklabels():
            label.set_rotation(rotation)


def ms2date(timestamps):
    dts = map(pl.datetime.fromtimestamp, timestamps/1000.0)
    return pl.date2num(dts) - 0.036

# Topics: line, color, LineCollection, cmap, colorline, codex
# http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
'''
Defines a function colorline that draws a (multi-)colored 2D line with coordinates x and y.
The color is taken from optional data in z, and creates a LineCollection.

z can be:
- empty, in which case a default coloring will be used based on the position along the input arrays
- a single number, for a uniform color [this can also be accomplished with the usual plt.plot]
- an array of the length of at least the same length as x, to color according to this data
- an array of a smaller length, in which case the colors are repeated along the curve

The function colorline returns the LineCollection created, which can be modified afterwards.

See also: plt.streamplot
'''
# Data manipulation:

def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    return segments


# Interface to LineCollection:
#http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
def colorline(x, y, z=None, cmap=pl.get_cmap('copper'), norm=pl.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    '''
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    '''

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm,
                        linewidth=linewidth, alpha=alpha)

    ax = pl.gca()
    ax.add_collection(lc)
    ax1 = pl.gcf().add_axes([0.95, 0.2, 0.05, 0.6])
    cb1 = ColorbarBase(ax1, cmap=cmap, norm=norm,
                                  orientation='vertical')
    return lc


def clear_frame(ax=None):
    # Taken from a post by Tony S Yu
    if ax is None:
        ax = pl.gca()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for spine in ax.spines.itervalues():
        spine.set_visible(False)


def axis_colorplot(m, ps, cmap=None, vmax=None, vmin=None, fmt='.3f', annot=False, ax=None,
                   tick_top=True, masked=False, **kwargs):
    if masked:
        mask = np.zeros_like(ps, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        kwargs['mask'] = mask

    cbar_kws = kwargs.pop('cbar_kws', {})
    if 'shrink' not in cbar_kws:
        cbar_kws['shrink'] = .5
    sn.heatmap(ps, cmap=cmap, vmax=vmax, fmt=fmt,
               square=True, xticklabels=m, yticklabels=m, vmin=vmin,
               linewidths=.5, cbar_kws=cbar_kws, annot=annot, ax=ax, **kwargs)
    if tick_top:
        pl.gca().xaxis.tick_top()


# http://mpastell.com/2009/05/11/iir-filter-design-with-python-and-scipy/
def irrfilter_response(b, a=1, nyquist=1, subfigures=[211, 212]):
    w, h = signal.freqz(b, a)
    h_dB = 20 * np.log10(abs(h))
    pl.subplot(subfigures[0])
    pl.plot(w/max(w) * nyquist, h_dB)
    pl.ylim(-150, 5)
    pl.ylabel('Magnitude [db]')
    pl.xlabel(r'Frequency [Hz]')
    pl.title(r'Frequency response')
    pl.subplot(subfigures[1])
    h_Phase = np.unwrap(np.arctan2(np.imag(h), np.real(h)))
    pl.plot(w/max(w) * nyquist, h_Phase)
    pl.ylabel('Phase [radians]')
    pl.xlabel(r'Frequency [Hz]')
    pl.title(r'Phase response')
    pl.subplots_adjust(hspace=0.5)


def hide_labels(x=False, y=False):
    if x:
        pl.setp(pl.gca().get_xticklabels(), visible=False)
    if y:
        pl.setp(pl.gca().get_yticklabels(), visible=False)


# https://stackoverflow.com/questions/4209467/matplotlib-share-x-axis-but-dont-show-x-axis-tick-labels-for-both-just-one
def label_outer():
    for ax in pl.gcf().axes:
        try:
            ax.label_outer()
        except Exception as e:
            # when this is printed, figure out the appropriate error type when
            # ax is not a subfigure and replace the too broad exception above
            print(str(e))


# https://stackoverflow.com/questions/13588920/stop-matplotlib-repeating-labels-in-legend
def remove_legend_duplicates(axis=None):
    axis = pl.gca() if axis is None else axis
    handles, labels = axis.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    pl.legend(by_label.values(), by_label.keys())