import filecmp
import multixrank
import os
import pathlib
import shutil
import unittest

from multixrank.PathManager import PathManager


class TestHetionet(unittest.TestCase):

    """Will test hetionet example"""

    def setUp(self):

        self.package_path = PathManager.get_package_path()
        self.test_path = PathManager.get_test_path()

        self.wdir = os.path.join(self.test_path, "test_data", 'hetionet')

        self.outdir = os.path.join(self.test_path, 'outdir')
        pathlib.Path(self.outdir).mkdir(exist_ok=True, parents=True)

    def test01_selfloops1(self):

        config_path = os.path.join(self.wdir, "config_full.yml")
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.wdir, 'outdir_bak_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])

    def tearDown(self):
        shutil.rmtree(self.outdir, ignore_errors=True)
