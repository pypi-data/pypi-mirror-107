from . import ewald, kernel, potentials

from numpy import testing
from unittest import TestCase


class NaClTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = kernel.Cell(
            [[0.5, 0.5, 0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]],
            [[0, 0, 0], [0.52, 0.52, 0.48]],
            ("na", "cl"),
            meta={"charges": [11, 17]},
        )
        cls.eta = 3

    def test_stats(self):
        v, c = ewald.stat_cell(self.cell)
        testing.assert_equal(v, 0.25)
        testing.assert_equal(c, 410)

    def __ewe__(self, eta, r, k):
        nw = kernel.NeighborWrapper(self.cell, cutoff=r, reciprocal_cutoff=k)
        p = potentials.ewald_total_potential_family(eta=eta, a=r, scale=1)
        return nw.total(p)

    def test_tol(self):
        r, k = ewald.ewald_cutoffs(self.eta, *ewald.stat_cell(self.cell))
        testing.assert_allclose(
            self.__ewe__(self.eta, r, k),
            self.__ewe__(self.eta, 2 * r, 2 * k),
        )

    def test_tol_direct(self):
        args = 0.2, 5, 6, 0.1
        r, k = ewald.ewald_cutoffs(*args, eps=1e-3)
        testing.assert_array_less(ewald.ewald_real_cutoff_error(r, *args), 1.1e-3)
        testing.assert_array_less(ewald.ewald_k_cutoff_error(k, *args), 1.1e-3)
