# silly-monte-carlo

## Overview

`silly-monte-carlo` is a small exercise in `monte-carlo` simulation.

### Quickstart...

```python

from smc import (abm, filesys, plots)

sim = abm.ArithmeticBrownianMotion(spot = 0.0, mu = 0.05, sigma = 0.2,
                                   timesteps = 128, paths = 256)

fig, _ = plots.simulation_summary(sim, 0.0, 1.0)
plots.save(fig, 'plots', 'abm', filesys.extension.pdf)
```

## Installation

As prerequisites, you will need git, and a suitable python version (`>=3.11`). 

```bash
# checkout repository.
git clone git@github.com:jjaemun/silly-monte-carlo.git
# go to library root.
cd silly-monte-carlo
# create and activate a python environment.
python -m venv .env
source .env/bin/activate
# build an editable install.
pip install -e .
```

The package is set up to dynamically install dependencies through the 
`requirements.txt` file. The editable install is sufficient to make available 
the local package and its runtime dependencies.

## API Surface

The `api` is quite small, and thus we only need to understand a few
elements to use the capabilities provided.

### Simulators

This is the core interface to generate `monte-carlo` paths. Its best that we
think of simulators as the source of truth for the stochastic models. The
properties they describe are the following:

```python

class Simulator(abc.ABC):
    
    def simulate(self, s: float, t: float,
                                 seed: Seed = None) -> sample.Sample:

        # `simulate` is the monte carlo path simulation 
        #  entry point.

        (...) 

    def mean(self, s: float, t: float) -> numpy.ndarray:

        # `mean` computes the theoretical expectation over
        # the simulation interval in [s, t].

        (...) 

    def variance(self, s: float, t: float) -> numpy.ndarray:

        # `variance` computes the theoretical dispersion 
        # over the simulation interval in [s, t].

        (...) 

    def autocovariance(self, s: float, t: float) -> numpy.ndarray:

        # `autocovariance` computes the theoretical 
        # autocovariance matrix over the interval [s, t].

        (...)
```

In all methods above `s` and `t` are the simulation interval boundaries. 
And so logically they should be (and we check that they are) ordered 
such that `s` < `t`. Methods dealing with time boundaries can raise exceptions.

#### Seeding

An intentional design choice was introducing optional seeding in the `simulation` method. 
There are two reasons for this:

    * allows reproducibility if we do decide to seed the `rng`; and,

    * it signals that we are dealing with rngs upon 
      calling this function but without taking ownership of the generators themselves.



### TimeGrid

`TimeGrid` models simulation time intervals. Given boundaries `s`, `t`, 
and a number of `timesteps`, it provides the grid values and the corresponding 
increment.

```python

@dataclass(frozen=True)
class TimeGrid:

    ''' Uniform time grid over an interval. '''

    s: float 
#   ^ start time
    t: float
#   ^ end time
    timesteps: int
#   ^^^^^^^^^ number of timesteps.

    @property
    def increment(self):

        # returns discrete time increment.
        # (...)

    @property
    def values(self):

        # returns discrete time grid.
        # (...)
```

### Sample

`Sample` is the simulation result type.

```python

@dataclass(frozen = True)
class Sample(object):

    ''' Result type for a monte carlo simulation. '''
    
    grid: TimeGrid
#   ^^^^ time grid.
    sims: numpy.ndarray
#   ^^^^ realized paths.

    @property
    def mean(self):

        # computes  sample mean.

    @property
    def variance(self):

        # computes sample variance.
```

It stores realized paths along with the `TimeGrid` on which they are
generated. Empirical moments are computed directly from the simulated paths.
This way, `simulators` remain in charge of theoretical moments
but never own or know anything about the results they produce.

## Models

The current model set is deliberately small.

| Model |
| --- |
| Arithmetic Brownian Motion |
| Geometric Brownian Motion |
