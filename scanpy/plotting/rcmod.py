"""Overwrite matplotlib's and seaborn's default rcParams.
"""

import matplotlib
from matplotlib import rcParams
from cycler import cycler

from . import palettes

def set_rcParams_scanpy(fontsize=14, color_map=None):
    """Set matplotlib.rcParams to Scanpy defaults."""

    # figure
    rcParams['figure.figsize'] = (4, 4)
    rcParams['figure.subplot.left'] = 0.18
    rcParams['figure.subplot.right'] = 0.96
    rcParams['figure.subplot.bottom'] = 0.15
    rcParams['figure.subplot.top'] = 0.91

    rcParams['lines.linewidth'] = 1.5
    rcParams['lines.markersize'] = 6
    rcParams['lines.markeredgewidth'] = 1

    # font
    rcParams['font.sans-serif'] = ['Arial',
                                   'Helvetica',
                                   'DejaVu Sans',
                                   'Bitstream Vera Sans',
                                   'sans-serif']
    fontsize = fontsize
    rcParams['font.size'] = fontsize
    rcParams['legend.fontsize'] = 0.92 * fontsize
    rcParams['axes.titlesize'] = fontsize
    rcParams['axes.labelsize'] = fontsize

    # legend
    rcParams['legend.numpoints'] = 1
    rcParams['legend.scatterpoints'] = 1
    rcParams['legend.handlelength'] = 0.5
    rcParams['legend.handletextpad'] = 0.4

    # color cycle
    rcParams['axes.prop_cycle'] = cycler(color=palettes.default_20)

    # lines
    rcParams['axes.linewidth'] = 0.8
    rcParams['axes.edgecolor'] = 'black'
    rcParams['axes.facecolor'] = 'white'

    # ticks
    rcParams['xtick.color'] = 'k'
    rcParams['ytick.color'] = 'k'
    rcParams['xtick.labelsize'] = fontsize
    rcParams['ytick.labelsize'] = fontsize

    # axes grid
    rcParams['axes.grid'] = True
    rcParams['grid.color'] = '.8'

    # color map  # seaborn 0.8.0 has 'rocket'
    rcParams['image.cmap'] = 'RdBu_r' if color_map is None else color_map


def set_rcParams_defaults():
    """Reset `matplotlib.rcParams` to defaults."""
    rcParams.update(matplotlib.rcParamsDefault)
