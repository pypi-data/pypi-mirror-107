from . import units
import unittest
import numericalunits as nu
import numpy as np
from numpy import testing


class TestArray(unittest.TestCase):
    def test_json_serialization(self):
        sample = np.array([0, 3, 1.4]) * nu.angstrom
        data = units.array_to_json(sample, units="angstrom")
        with units.new_units_context():
            nu.reset_units()
            test = units.array_from_json(data)
            testing.assert_allclose(test, np.array([0, 3, 1.4]) * nu.angstrom)


class TestUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.units = units.UnitsDict({"a": "angstrom", "r": "Ry", "something": "1/angstrom**2"})

    def test_apply(self):
        angstrom = nu.angstrom
        Ry = nu.Ry
        self.assertEqual(self.units.apply({"a": 2 * angstrom, "r": (2 * Ry, 3 * Ry), "x": 2}),
                         {"a": 2 * angstrom / angstrom, "r": (2 * Ry / Ry, 3 * Ry / Ry), "x": 2})
        self.assertEqual(self.units.apply({"a": (1 * angstrom, 3 * angstrom), "r": None}),
                         {"a": (1, 3 * angstrom / angstrom), "r": None})

    def test_lift(self):
        self.assertEqual(self.units.lift({"a": 2, "r": 3, "x": 2}), {"a": 2 * nu.angstrom, "r": 3 * nu.Ry, "x": 2})
        self.assertEqual(self.units.lift({"a": (1, 3), "r": None}), {"a": (1 * nu.angstrom, 3 * nu.angstrom), "r": None})

    def test_eval(self):
        self.assertEqual(self.units.get_uv("a"), nu.angstrom)
        self.assertEqual(self.units.get_uv("something"), 1 / nu.angstrom ** 2)

    def test_default_units(self):
        with units.new_units_context():
            units.init_default_atomic_units()
            testing.assert_allclose(nu.angstrom, 1)
            testing.assert_allclose(nu.eV, 1)
