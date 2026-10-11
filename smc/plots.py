# -*- coding: utf-8 -*-


from . import (filesys, sample, simulator, cfg)


import os
from matplotlib import (pyplot, axes, figure)


from typing import Optional


# --update.
pyplot.rcParams.update(cfg.PLOT_CFG)


def dbg_show(*_: ..., **__: ...):
    
    ''' Shows recorded plots, ignore. '''
    
    pyplot.show()

def save(fig: figure.Figure, fspath: os.PathLike, 
                             filename: str, e: filesys.extension):

    ''' Writes to disc the generated plot. '''
    
    fspath = os.path.join(fspath, filename + e.value)
    fig.savefig(fspath)


def simulation_summary(sim: simulator.Simulator, s: float, t: float):

    ''' Plot paths againts theoretic moments. '''

    sampled = sim.simulate(s, t)

    (fig, axs) = pyplot.subplots(3, 1, sharex = True)
    (sax, eax, vax) = axs

    paths(sampled, sax)
    mean(sim, sampled, s, t, eax)
    variance(sim, sampled, s, t, vax)

    sax.set_title(type(sim).__name__)
    sax.text(1.02, 1.0, _tabular(sim), transform = sax.transAxes,
            va = 'top', ha = 'left', fontsize = 8, family = 'monospace')
    vax.set_xlabel("time")

    fig.tight_layout()

    return fig, (sax, eax, vax)


def paths(sampled: sample.Sample, ax: Optional[axes.Axes] = None):
    
    ''' Plots simulated paths. If no ax is provided, it
            generates and plots its own. '''
    
    if (ax) is None:
        (_, ax) = pyplot.subplots()

    for path in sampled.sims:
        ax.plot(sampled.grid.values, path, **cfg.LINESTYLE)
    
    ax.set_ylabel('paths')
    return ax


def mean(sim: ..., sampled: sample.Sample, s: float, 
                   t: float, ax: Optional[axes.Axes] = None):

    ''' plots empirical and theoretic mean paths. '''

    if (ax) is None:
        (_, ax) = pyplot.subplots()

    ax.plot(sampled.grid.values, sampled.mean, 
            label = 'empirical', **cfg.LINESTYLE)
    ax.plot(sampled.grid.values, sim.mean(s, t), 
            label = 'theoretic', color = 'black', **cfg.LINESTYLE)

    ax.set_ylabel('mean')
    ax.legend()

    return ax


def variance(sim: ..., sampled: sample.Sample, s: float, 
                       t: float, ax: Optional[axes.Axes] = None):

    ''' Plots empirical and theoretic variance paths. '''

    if (ax) is None:
        (_, ax) = pyplot.subplots()

    ax.plot(sampled.grid.values, sampled.variance, 
            label = 'empirical', **cfg.LINESTYLE)
    ax.plot(sampled.grid.values, sim.variance(s, t), 
            label = 'theoretic', color = 'black', **cfg.LINESTYLE)

    ax.set_ylabel('variance')
    ax.legend()

    return ax


def _tabular(sim: simulator.Simulator) -> str:

    ''' Tabular format for simulator params. '''

    items = vars(sim).items()
    width = max(len(key) for key, _ in items)

    return '\n'.join(f'{key:<{width}}: {value!r}' for key, value in items)



