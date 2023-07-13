import filecmp

import numpy
import pandas

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
        # self.assertEqual(filecmp.dircmp(outdir_path, outdir_path_bak).diff_files, [])
        multiplex_2_path = os.path.join(outdir_path, "multiplex_2.tsv")
        multiplex_2_path_bak = os.path.join(outdir_path_bak, "multiplex_2.tsv")
        # self.assertTrue(filecmp.cmp(multiplex_2_path, multiplex_2_path_bak))
        multiplex_2_df = pandas.read_csv(multiplex_2_path, sep="\t")
        multiplex_2_df_bak = pandas.read_csv(multiplex_2_path_bak, sep="\t")
        multiplex_2_score_lst = multiplex_2_df['score'].tolist()
        multiplex_2_score_lst_bak = multiplex_2_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_2_score_lst, multiplex_2_score_lst_bak, decimal=7)

        multiplex_3_path = os.path.join(outdir_path, "multiplex_3.tsv")
        multiplex_3_path_bak = os.path.join(outdir_path_bak, "multiplex_3.tsv")
        # self.assertTrue(filecmp.cmp(multiplex_3_path, multiplex_3_path_bak))
        multiplex_3_df = pandas.read_csv(multiplex_3_path, sep="\t")
        multiplex_3_df_bak = pandas.read_csv(multiplex_3_path_bak, sep="\t")
        multiplex_3_score_lst = multiplex_3_df['score'].tolist()
        multiplex_3_score_lst_bak = multiplex_3_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_3_score_lst, multiplex_3_score_lst_bak, decimal=7)

    def tearDown(self):
        shutil.rmtree(self.outdir, ignore_errors=True)
