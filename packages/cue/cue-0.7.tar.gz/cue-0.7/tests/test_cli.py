import subprocess, os
from pathlib import Path

from tests.unit_test import UnitTest


class TestCli(UnitTest):

    def test_cli_bin_1(self):
        """cue parses command line args"""
        sp = subprocess.run(['cue', 'echo', 'test', 'bin'],
                            capture_output=True)
        assert sp.stdout.decode('utf-8').strip() == 'test bin'
