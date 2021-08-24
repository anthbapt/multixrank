import filecmp
import logging
import multixrank
import os
import pathlib
import shutil
import unittest

from multixrank.logger_setup import logger
from multixrank.PathManager import PathManager

logger.setLevel(logging.INFO)  # set root's level

class TestBiological(unittest.TestCase):

    """Will test biological example"""

    def setUp(self):

        self.package_path = PathManager.get_package_path()
        self.test_path = PathManager.get_test_path()

        self.biological_dir_path = os.path.join(self.test_path, "test_data", 'biological')

        self.outdir = os.path.join(self.test_path, 'outdir')
        pathlib.Path(self.outdir).mkdir(exist_ok=True, parents=True)

    def test01_config_minimal_default(self):
        """Fully default/homogeneous parameters"""

        config_path = os.path.join(self.test_path, "test_data", "biological", "config_minimal_default.yml")
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.biological_dir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'biological', 'outdir_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])

    def test01_config_full_default(self):
        """Minimal config to test default/homogeneous parameters"""

        config_path = os.path.join(self.test_path, "test_data", "biological", "config_full_default.yml")
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.biological_dir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'biological', 'outdir_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])

    def test01_selfloops1(self):

        config_path = os.path.join(self.test_path, "test_data", "biological", "config.yml")
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.biological_dir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'biological', 'outdir_ranking01')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])

    def test01_selfloops0(self):

        config_path = os.path.join(self.test_path, "test_data",
                                           "biological", "config_self_loops0.yml")
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.biological_dir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'biological', 'outdir_ranking01_selfloops0')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])

    def tearDown(self):
        # shutil.rmtree(self.biological_dir_path, ignore_errors=True)
        shutil.rmtree(self.outdir, ignore_errors=True)
