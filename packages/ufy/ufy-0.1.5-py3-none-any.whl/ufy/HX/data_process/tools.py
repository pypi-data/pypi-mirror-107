# -*- coding: utf-8 -*-
# @Time     : 2021/5/17 13:23
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : tools.py
# @info     :

from typing import List

from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from udata import UData


class Data(UData):
    def __init__(self, datafile: str) -> None:
        print('load data:', datafile)
        self.data = self.read(datafile)

    def select_data_by_list(self, choose_list: List, choose_col: str, savename='select.xlsx',
                            index_save: bool = False) -> (DataFrame, List):
        '''
        :param choose_list: 需要筛选的list
        :param choose_col: 筛选列
        :param savename: 结果保存名
        :param index_save: 是否保存index 列
        :return: 筛选后的的结果和没有找到的list
        '''
        choose_index = []
        finds = []
        for i in tqdm(range(len(self.data))):
            if self.data.loc[i, choose_col] in choose_list:
                choose_index.append(i)
                finds.append(self.data.loc[i, choose_col])
                choose_list.remove(self.data.loc[i, choose_col])

        notfinds = []
        for item in choose_list:
            if item not in finds:
                notfinds.append((item))

        out = self.data.loc[choose_index]
        self.save(data=out, savename=savename, index=index_save)
        return out, notfinds
