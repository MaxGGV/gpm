# -*- coding: UTF-8 -*-

# Import from standard library
import os
import random
import unittest

import gpm
import pandas as pd
# Import from our lib
from gpm.online import get_insee_batch



def get_local_data():
    datapath = os.path.dirname(os.path.abspath(gpm.__file__)) + '/data'
    file_path = '{}/test_sample.csv'.format(datapath)
    df = pd.read_csv(file_path)
    l_insee = df.pop('code_insee').to_list()
    return df, l_insee


class TestUtils(unittest.TestCase):

    @unittest.skip('')
    def test_get_insee_batch(self):
        datapath = os.path.dirname(os.path.abspath(gpm.__file__)) + '/data'
        file_path = '{}/test_sample.csv'.format(datapath)
        df = get_insee_batch(csv_path=file_path, save=False, sep=',')
        res = list(df.code_insee)
        expected = pd.read_csv('{}/test_sample_codeinsee.csv'.format(datapath)).code_insee.to_list()
        df['ex_code_insee'] = expected
        print(df[df.code_insee != df.ex_code_insee])
        self.assertEqual(res, expected)

    def test_get_insee_groupama_data(self):
        datapath = os.path.dirname(os.path.abspath(gpm.__file__)) + '/data'
        file_path = '{}/groupama_input.csv'.format(datapath)
        df = get_insee_batch(csv_path=file_path, save=False, sep=';')
        res = list(df.code_insee)
        expected = [78397, 61006, 72181]
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
