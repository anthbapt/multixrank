import filecmp
import logging

import numpy
import pandas

import multixrank
import os
import pathlib
import shutil
import unittest

from multixrank.logger_setup import logger
from multixrank.PathManager import PathManager

logger.setLevel(logging.INFO)  # set log level


class TestAirport(unittest.TestCase):

    """Will test airport example"""

    def setUp(self):

        self.package_path = PathManager.get_package_path()
        self.test_path = PathManager.get_test_path()

        self.wdir_path = os.path.join(self.package_path, 'data_example', 'airport')

        self.outdir = os.path.join(self.test_path, 'outdir')
        pathlib.Path(self.outdir).mkdir(exist_ok=True, parents=True)

        self.precision = 10

    def test_airport_minimal(self):

        config_path = os.path.join(self.package_path, 'data_example', 'airport', 'config_minimal.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_one_multiplex_fr(self):

        wdir = os.path.join(self.package_path, 'data_example', 'airport')
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_one_multiplex_fr.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_one_multiplex_fr')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_change_bipartite_source_target_columns(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_change_bipartite_source_target_columns.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_bipartite3cols(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_bipartite3cols.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_multiplex3cols(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_multiplex3cols.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_weighted(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.package_path, 'tests', 'test_data', 'airport', 'config_minimal_weighted.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_sif_top3(self):

        config_path = os.path.join(self.package_path, 'data_example', 'airport', 'config_minimal.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        out_path = os.path.join(self.test_path, 'outdir', 'ranking_default_top3.sif')
        out_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_top3.sif')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.to_sif(rwr_df, path=out_path, top=3)
        # import pdb; pdb.set_trace()
        self.assertTrue(filecmp.cmp(out_path, out_path_bak))

    def test_airport_minimal_directed(self):

        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_directed.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_directed')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_directed_degree(self):

        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_directed.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_directed_degree')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path, degree=True)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_directed_degree_top5(self):

        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_directed.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_directed_degree_top5')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path, top=5, degree=True)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_degree(self):

        config_path = os.path.join(self.package_path, 'data_example', 'airport', 'config_minimal.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_degree')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path, degree=True)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_full(self):

        config_path = os.path.join(self.package_path, 'data_example', 'airport', 'config_full.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_multiplex_self_loops_false(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_multiplex_self_loops_false.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_multiplex_self_loops_true(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_multiplex_self_loops_true.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)

        multiplex_1_path = os.path.join(self.test_path, 'outdir', 'ranking_default', 'multiplex_1.tsv')
        multiplex_1_bak_path = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'multiplex_1_self_loops_true.tsv')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=os.path.dirname(multiplex_1_path))
        # import pdb; pdb.set_trace()
        # self.assertTrue(filecmp.cmp(multiplex_1_path, multiplex_1_bak_path, shallow=True))
        multiplex_1_df_bak = pandas.read_csv(multiplex_1_bak_path, sep="\t")
        multiplex_1_df = pandas.read_csv(multiplex_1_path, sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_bipartite_self_loops_false(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_bipartite_self_loops_false.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)
        self.assertFalse('999' in multixrank_obj.__dict__['bipartiteall_obj'].__dict__[
            'source_target_bipartite_dic'][('1', '2')].networkx.nodes)

    def test_airport_minimal_bipartite_self_loops_true(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_bipartite_self_loops_true.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)
        self.assertTrue('999' in multixrank_obj.__dict__['bipartiteall_obj'].__dict__[
            'source_target_bipartite_dic'][('1', '2')].networkx.nodes)

    def test_airport_minimal_2bipartites(self):

        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_2bipartites.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=self.wdir_path)

        outdir_path = os.path.join(self.test_path, 'outdir', 'ranking_default')
        outdir_path_bak = os.path.join(self.test_path, 'test_data', 'airport', 'outdir_bak', 'ranking_default_2bipartites')
        rwr_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(rwr_df, path=outdir_path)
        # import pdb; pdb.set_trace()
        multiplex_1_df_bak = pandas.read_csv(os.path.join(outdir_path_bak, "multiplex_1.tsv"), sep="\t")
        multiplex_1_df = pandas.read_csv(os.path.join(outdir_path, "multiplex_1.tsv"), sep="\t")
        multiplex_1_score_lst = multiplex_1_df['score'].tolist()
        multiplex_1_score_lst_bak = multiplex_1_df_bak['score'].tolist()
        numpy.testing.assert_almost_equal(multiplex_1_score_lst, multiplex_1_score_lst_bak, self.precision)

    def test_airport_minimal_multiplex_no_edges(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_multiplex_only_self_loops.yml')
        with self.assertRaises(SystemExit) as cm:
            logging.disable(logging.ERROR)
            multixrank.Multixrank(config=config_path, wdir=wdir)
            logging.disable(logging.NOTSET)
        self.assertEqual(cm.exception.code, 1)

    def test_airport_minimal_bipartite_no_edges(self):

        wdir = os.path.join(PathManager.get_package_path())
        config_path = os.path.join(self.test_path, 'test_data', 'airport', 'config_minimal_bipartite_only_self_loops.yml')
        multixrank_obj = multixrank.Multixrank(config=config_path, wdir=wdir)
        with self.assertRaises(SystemExit) as cm:
            logging.disable(logging.ERROR)
            rwr_df = multixrank_obj.random_walk_rank()
            logging.disable(logging.NOTSET)
        self.assertEqual(cm.exception.code, 1)

    def tearDown(self):
        shutil.rmtree(self.outdir, ignore_errors=True)
