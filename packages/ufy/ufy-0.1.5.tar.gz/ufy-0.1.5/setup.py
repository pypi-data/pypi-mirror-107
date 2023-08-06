# -*- coding: utf-8 -*-
# @Time     : 2021/4/22 19:36
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : setup.py.py
# @info     :

from setuptools import setup

__version__ = '0.1.5'

setup(name='ufy',
      version=__version__,
      description='some tools for ufy',
      author='ufy',
      author_eamil='antarm@outlook.com',
      url='https://github.com/antarm/ufy',
      packages=['ufy',
                'ufy.core','ufy.core.DataStructure', 'ufy.core.ML', 'ufy.core.DL', 'ufy.core.ML.compaction', 'ufy.core.preprocessing','ufy.core.utils',
                'ufy.CV',
                'ufy.datasets',
                'ufy.HX', 'ufy.HX.data_process','ufy.HX.diagnosis'])
