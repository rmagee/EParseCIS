#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_eparsecis
----------------------------------

Tests for `eparsecis` module.
"""

from io import StringIO, BytesIO
import os
import logging
import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from eparsecis import eparsecis
from eparsecis import cli



class TestEparsecis(unittest.TestCase):


    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'eparsecis.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_epcis_file(self):
        curpath = os.path.dirname(__file__)
        parser = eparsecis.FastIterParser(os.path.join(curpath, 'data/epcis.xml'))
        parser.parse()

