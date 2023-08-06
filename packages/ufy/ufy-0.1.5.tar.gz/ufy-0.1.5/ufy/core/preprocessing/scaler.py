# -*- coding: utf-8 -*-
# @Time     : 2021/5/13 17:01
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : scaler.py
# @info     : 本模块集成各种归一化或标准化方法

from ufy.np import np

'''
'''
class Standard_scaler():
    def __init__(self):
        self.__mean = None
        self.__std = None

    def fit(self, X: np.ndarray, axis: tuple):
        self.__mean = np.mean(X, axis=axis)
        self.__std = np.std(X, axis=axis)

    def transform(self, X: np.ndarray):
        assert self.__mean is not None and self.__std is not None, 'must fit before transform!'

        epsilon = 1e-7
        out = (X - self.__mean) / (self.__std + epsilon)
        return out


class Min_max_scaler():
    def __init__(self):
        self.__min = None
        self.__std = None

    def fit(self, X: np.ndarray, axis: tuple):
        self.__min = np.min(X, axis=axis)
        self.__max = np.max(X, axis=axis)

    def transform(self, X: np.ndarray):
        assert (self.__min is not None) and (self.__max is not None), 'must fit before transform!'

        epsilon = 1e-7
        out = (X - self.__min) / (self.__max - self.__min + epsilon)
        return out
