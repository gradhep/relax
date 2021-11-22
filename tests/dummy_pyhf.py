import jax.numpy as jnp
import pyhf


# class-based
class _Config:
    def __init__(self):
        self.poi_index = 0
        self.npars = 2

    def suggested_init(self):
        return jnp.asarray([1.0, 1.0])

    def suggested_bounds(self):
        return jnp.asarray([jnp.asarray([0.0, 10.0]), jnp.asarray([0.0, 10.0])])


class Model:
    """Dummy class to mimic the functionality of `pyhf.Model`."""

    def __init__(self, spec):
        self.sig, self.nominal, self.uncert = spec
        self.factor = (self.nominal / self.uncert) ** 2
        self.aux = 1.0 * self.factor
        self.config = _Config()

    def expected_data(self, pars):
        mu, gamma = pars
        expected_main = jnp.asarray([gamma * self.nominal + mu * self.sig])
        aux_data = jnp.asarray([self.aux])
        return jnp.concatenate([expected_main, aux_data])

    def logpdf(self, pars, data):
        maindata, auxdata = data
        main, _ = self.expected_data(pars)
        _, gamma = pars
        main = pyhf.probability.Poisson(main).log_prob(maindata)
        constraint = pyhf.probability.Poisson(gamma * self.factor).log_prob(auxdata)
        # sum log probs over bins
        return jnp.asarray([jnp.sum(main + constraint, axis=0)])


def uncorrelated_background(signal_data, bkg_data, bkg_uncerts):
    """Dummy class to mimic the functionality of `pyhf.simplemodels.hepdata_like`."""
    return Model([signal_data, bkg_data, bkg_uncerts])
