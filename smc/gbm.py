# -*- coding: utf-8 -*-


import numpy
from . import (check, simulator, sample, seeding, timegrid)


class GeometricBrownianMotion(simulator.Simulator):

    ''' Geometric brownian motion (gbm) monte
            carlo simulator. '''

    def __init__(self, spot: float, mu: float, sigma: float, 
                       timesteps: int, paths: int):
        self.spot = spot
        self.mu = mu
        self.sigma = sigma 

        # Notes
        #
        # We assert that `timesteps` and `paths` be 
        # positive integers. 

        check.positive_integer(timesteps)
        check.positive_integer(paths)

        self.timesteps = timesteps
        self.paths = paths


    def simulate(self, s: float, t: float,
                       seed: seeding.Seed = None) -> sample.Sample:

        '''  Computes synthetic paths over simulation 
                period [s, t]. '''

        rng = numpy.random.default_rng(seed)
        
        grid = timegrid.TimeGrid(s, t, self.timesteps)
        gaussians = (numpy.sqrt(grid.increment) 
                        * rng.normal(size = (self.paths, self.timesteps)))
        
        drift = (self.mu - self.sigma * self.sigma / 2) * grid.increment
        diffusion = self.sigma * gaussians

        ds = numpy.concatenate([numpy.zeros((self.paths, 1)), 
                                drift + diffusion], axis=1)
        log = numpy.cumsum(ds, axis = 1)

        return sample.Sample(grid = grid, 
                             sims = self.spot * numpy.exp(log))


    def mean(self, s: float, t: float) -> ...:
        
        ''' Computes theoretic path of one-time first order 
                moments over the period [s, t]. '''

        grid = timegrid.TimeGrid(s, t, self.timesteps)
        return self.spot * numpy.exp(self.mu * (grid.values - s))


    def variance(self, s: float, t: float) -> ...: 

        ''' Returns theoretic dispersion over the 
                period  [s, t].'''

        grid = timegrid.TimeGrid(s, t, self.timesteps)
        correction = (numpy.exp(self.sigma * self.sigma 
                        * (grid.values - s)) - 1)

        return correction * (self.spot * self.spot 
                    * numpy.exp(2 * self.mu * (grid.values - s)))

             

    def autocovariance(self, s: float, t: float) -> ...:

        ''' Returns theoretic mixed second order central  
                moments on times s, t. '''
        
        grid = timegrid.TimeGrid(s, t, self.timesteps)
        
        mean = self.mean(s, t)
        mini = numpy.minimum.outer(grid.values - s, grid.values - s)

        return (numpy.outer(mean, mean) *
                    (numpy.exp(self.sigma * self.sigma * mini) - 1))
