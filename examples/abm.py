# -*- coding: utf-8 -*-


from smc import (abm, plots)


sim = abm.ArithmeticBrownianMotion(spot = 0.0, mu = 0.05, sigma = 0.2,
                                   timesteps = 128, paths = 24)

fig, _ = plots.simulation_summary(sim, 0.0, 1.0)
plots.dbg_show(fig)
