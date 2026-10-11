# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
from typing import Dict, Any


PLOT_CFG: Dict[str, Any] = {

    # Base plot cfg.
        
    # always grid
    'axes.grid': True,

    # grid lines
    'grid.linestyle': 'dotted',

    # figure size
    'figure.figsize': (7, 10),
}


TRY_PLOT_CFG: Dict[str, Any] = {

    # Possibly breaking plot cfg.

    # latex formatting
    #
    # Notes
    #
    # Possibly a breaking feature if matplot cannot
    # find a local distribution.
    'text.usetex': True,

    # grid lines
    'grid.linestyle': 'dotted',

    # figure size
    'figure.figsize': (7, 5),

    # font
    'font.family': 'Computer Modern Roman',
}


LINESTYLE: Dict[str, Any] = {

    # Line style configurations.
   
    # transparency
    'alpha': 0.5,

    # line width
    'linewidth': 1.0,
}
