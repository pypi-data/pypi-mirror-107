from . import util

import numpy as np
from numpy import testing
import numericalunits as nu
from unittest import TestCase


class TestUtil(TestCase):
    def test_num_grad(self):
        def f(_x, _a):
            return (_x ** 2).sum() * _a

        x = np.array([[1, 2, 3], [4, 5, 6]])
        testing.assert_allclose(util.num_grad(f, x, 2), 4 * x)

    def test_masked_unique(self):
        test_masked = [
            np.ma.masked_array(data=[4, 5, 2, 1], mask=[0, 0, 1, 0], fill_value=1),
            np.ma.masked_array(data=[4, 5, 1, 1], mask=[0, 0, 1, 0], fill_value=1),  # make an intentional collision
        ]

        for a in test_masked:
            key, inverse = util.masked_unique(a, return_inverse=True)
            testing.assert_equal(key, [1, 4, 5], err_msg=repr(a))
            testing.assert_equal(inverse.mask, a.mask, err_msg=repr(a))
            testing.assert_equal(inverse.data, [1, 2, 3, 0], err_msg=repr(a))
            testing.assert_equal(inverse.mask, [0, 0, 1, 0], err_msg=repr(a))

    def test_masked_unique_char(self):
        test_masked = [
            np.ma.masked_array(data=['d', 'e', 'b', ''], mask=[0, 0, 1, 0]),
            np.ma.masked_array(data=['d', 'e', '', ''], mask=[0, 0, 1, 0]),  # make an intentional collision
        ]

        for a in test_masked:
            key, inverse = util.masked_unique(a, return_inverse=True)
            testing.assert_equal(key, ['', 'd', 'e'], err_msg=repr(a))
            testing.assert_equal(inverse.mask, a.mask, err_msg=repr(a))
            testing.assert_equal(inverse.data, [1, 2, 3, 0], err_msg=repr(a))
            testing.assert_equal(inverse.mask, [0, 0, 1, 0], err_msg=repr(a))
