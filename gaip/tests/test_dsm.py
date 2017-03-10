#!/usr/bin/env python
"""
Unittesting framework for the `gaip.get_dsm` function.
"""

from __future__ import absolute_import
import unittest
import argparse
from argparse import RawTextHelpFormatter

import numpy.testing as npt
import h5py

from gaip.tests.unittesting_tools import ParameterisedTestCase


class TestDsm(ParameterisedTestCase):
    """
    Unittesting for the dsm extraction and smoothing
    found in `gaip.get_dsm`.

    Unittests will occur for the following datasets:

        * dsm
        * dsm-smoothed-exiting

    We're not explicitly testing the function, but implicitly
    testing the function by comparing against an existing
    dataset.
    """

    def test_dsm(self):
        """
        Test the extracted dsm.
        """
        with h5py.File(self.reference_fname, 'r') as reference_fid,\
            h5py.File(self.test_fname, 'r') as test_fid:

            ref_dset = reference_fid['dsm']
            test_dset = test_fid['dsm']

            npt.assert_almost_equal(test_dset, ref_dset,
                                    decimal=self.decimal_precision)

    def test_smoothed_dsm(self):
        """
        Test the smoothed dsm.
        """
        with h5py.File(self.reference_fname, 'r') as reference_fid,\
            h5py.File(self.test_fname, 'r') as test_fid:

            ref_dset = reference_fid['dsm-smoothed']
            test_dset = test_fid['dsm-smoothed']

            npt.assert_almost_equal(test_dset, ref_dset,
                                    decimal=self.decimal_precision)


if __name__ == '__main__':
    description = ("Unittests for `gaip.get_dsm` function.\n"
                   "Comparisons tests will occur for the following "
                   "datasets: \n"
                   "\t* dsm\n"
                   "\t* dsm-smoothed\n")
                   
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('--reference_fname', requried=True,
                        help=('The filename containing the reference datasets '
                              'to be used as a baseline.'))
    parser.add_argument('--test_fname', require=True,
                        help=('The filename containing the test datasets '
                              'to be used in comparing against the '
                              'base/reference datasets.'))
    parser.add_argument('--decimal_precision', default=4, type=int,
                        help=('The decimal precision used for the comparison '
                              'of images.'))
    parser.add_argument('--integer_precision', default=1, type=int,
                        help=('The integer precision used for the comparison '
                              'of images.'))

    parsed_args = parser.parse_args()

    reference_fname = parsed_args.reference_fname
    test_fname = parsed_args.test_fname
    decimal_precision = parsed_args.decimal_precision
    integer_precision = parsed_args.integer_precision

    suite = unittest.TestSuite()
    test_case = ParameterisedTestCase()
    suite.addTest(test_case.parameterise(TestDsm,
                                         reference_fname=reference_fname,
                                         test_fname=test_fname,
                                         decimal_precision=decimal_precision,
                                         integer_precision=integer_precision))
    unittest.TextTestRunner(verbosity=2).run(suite)