#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_eparsecis
----------------------------------

Tests for `eparsecis` module.
"""
import os
import logging
import unittest

from eparsecis import eparsecis


class TestEparsecis(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_epcis_file(self):
        curpath = os.path.dirname(__file__)
        parser = eparsecis.FastIterParser(
            os.path.join(curpath, 'data/epcis.xml'))
        parser.parse()
