#!/usr/bin/env python

"""Tests on the pydoni package file and folder structure."""

import pydoni
import re
import unittest
from os import chdir, remove
from os.path import dirname, join, abspath, expanduser, splitext, isfile, isdir, basename


class TestPackageStructure(unittest.TestCase):
    """
    Tests for pydoni package file and folder structure.
    """
    def test_version(self):

        with open(join(root_dir, 'setup.py')) as f:
            setup_py_contents = f.read().split()
            setup_py_version_str = [x for x in setup_py_contents if 'version' in x][0]
            setup_py_version = setup_py_version_str.replace('version=', '').replace(',', '').replace("'", '')

        with open(join(root_dir, 'setup.cfg')) as f:
            setup_cfg_contents = f.read().split('\n')
            setup_cfg_version_str = [x for x in setup_cfg_contents if 'current_version' in x][0]
            setup_cfg_version = setup_cfg_version_str.split('=')[1].strip()

        with open(join(root_dir, 'pydoni', '__init__.py')) as f:
            init_py_contents = f.read().split('\n')
            init_py_version_str = [x for x in init_py_contents if '__version__' in x][0]
            init_py_version = init_py_version_str.split('=')[1].replace("'", '').strip()


        self.assertEqual(setup_py_version, setup_cfg_version,
                         msg='Version numbers in setup.py and setup.cfg are out of sync!')
        self.assertEqual(setup_py_version, init_py_version,
                         msg='Version numbers in setup.py and __init__.py are out of sync!')
        self.assertEqual(setup_cfg_version, init_py_version,
                         msg='Version numbers in setup.cfg and __init__.py are out of sync!')

    def test_test_data_folder(self):
        test_data_fpaths = pydoni.listfiles(path=join(tests_dir, 'test_data'),
                                            recursive=True,
                                            include_hidden=False)
        for fpath in test_data_fpaths:
            fpath_relative = re.sub(r'(.*?)(test_data\/)(.*)', r'\2\3', fpath)
            self.assertTrue(basename(fpath_relative).startswith('test_'),
                            msg=f'File "{fpath_relative}" does not start with "test_"')


tests_dir = dirname(abspath(__file__))
root_dir = dirname(tests_dir)
chdir(root_dir)

case = TestPackageStructure()

test_methods = [x for x in dir(case) if x.startswith('test_')]
for method in test_methods:
    getattr(case, method)()
