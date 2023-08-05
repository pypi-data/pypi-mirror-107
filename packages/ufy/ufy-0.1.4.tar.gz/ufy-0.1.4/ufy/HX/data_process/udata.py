# -*- coding: utf-8 -*-
# @Time     : 2021/5/24 17:22
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : udata.py
# @info     :

import pandas as pd
from pandas import DataFrame


class UData:
    def read(self, datafile: str) -> None:
        if datafile.endswith('.xlsx'):
            self.data = pd.read_excel(datafile)
        elif datafile.endswith('.csv'):
            self.data = pd.read_csv(datafile)
        else:
            self.data = DataFrame()
            raise ValueError('This methods is only support ".xlsx" and ".csv" files, please check your filename again.')

    def save(self, data: DataFrame, savename: str, index=False) -> None:
        if savename.endswith('.xlsx'):
            data.to_excel(savename, index=index)
        elif savename.endswith('.csv'):
            data.to_csv(savename, index=index)
        else:
            raise ValueError(
                'Can not save, please check your savename is correct. We just support ".xlsx" and ".csv" file.')
