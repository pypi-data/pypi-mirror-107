# -*- coding: utf-8 -*-
# @Time     : 2021/5/12 11:52
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : data_map.py
# @info     : 本模块用于处理文件映射： 映射关系： sickNo <- pathologyNum（图片信息） <- 片子名

# note      : 病理号格式：pre+year+num+subnum，其中主号包括pre+year+num
import datetime
import os
import re
import shutil

import pandas as pd
from pandas import DataFrame
import numpy as np
from tqdm import tqdm

default_pre = 'Z'

from typing import List


def clear_str(s: str, drop_char: List[str] = ['.']):
    for c in drop_char:
        s = s.replace(c, '')
    return s


def check_and_getsubNum(s, default_pre='Z', num_bit=5, drop_char=['.']):
    ''' 判断病理号是否合理并，并返回病理主号+副号
        :param s: 病理号字符串
        :param default_pre: 默认前缀，当字符串没有前缀时，默认前缀为Z
        :param num_bit: 编号位数限制（默认不能超过5位）
        :param drop_char: 需要去除的无效字符
        :return:
    '''
    if not isinstance(s, str) or (s == ''):
        return False, []

    s = s.upper()  # 统一处理为大写
    s = clear_str(s, drop_char=drop_char)  # 统一处理干扰字符

    pre, year, num, subnum = '', '', '', ''
    i = 0

    # 获取前缀信息：pre
    if not str.isalpha(s[0]):
        pre = default_pre
    else:
        while (i < len(s)) and str.isalpha(s[i]):
            pre += s[i]
            i += 1

    # 获取年份信息：year
    if len(s) - i < 3:
        return False, []
    if str.isdigit(s[i:i + 2]):
        year = s[i:i + 2]
        i += 2
    elif str.isdigit(s[i]):
        year = s[i]
        i += 1
    else:
        return False, []

    # 获取编号：num
    while (i < len(s)) and (not str.isdigit(s[i])):
        i += 1
    while (i < len(s)) and (str.isdigit(s[i])):
        num += s[i]
        i += 1
    if len(num) > num_bit:  # 超出位数，为不规范的编号
        return False, []

    # 获取副号：subnum
    while (i < len(s)) and (not str.isdigit(s[i])):
        i += 1
    while (i < len(s)) and (str.isdigit(s[i])):
        subnum += s[i]
        i += 1

    # print(pre, year, num, subnum)
    if subnum == '':
        return True, [pre, int(year), int(num), None]
    else:
        return True, [pre, int(year), int(num), int(subnum)]


def check_and_getmainNum(s, default_pre='Z', num_bit=5, drop_char=['.']):
    ''' 判断病理号是否合理并，并返回病理主号
    :param s: 病理号字符串
    :param default_pre: 默认前缀，当字符串没有前缀时，默认前缀为Z
    :param num_bit: 编号位数限制（默认不能超过5位）
    :param drop_char: 需要去除的无效字符
    :return:
    '''

    flag, subNum = check_and_getsubNum(s, default_pre, num_bit, drop_char)

    if not flag:
        return flag, []
    else:
        return flag, subNum[:3]


def check_and_getmainNum_multi(s, default_pre='Z', num_bit=5, drop_char=['.']) -> (bool, List):
    ''' 判断病理号是否合理并，并返回病理主号(多个病理号)
    :param s: 病理号字符串,可能含多个病理号
    :param default_pre: 默认前缀，当字符串没有前缀时，默认前缀为Z
    :param num_bit: 编号位数限制（默认不能超过5位）
    :param drop_char: 需要去除的无效字符
    :return:
    '''
    if not isinstance(s, str):
        return False, []
    else:
        arr = re.split('、|/|,', s)
        check = False
        mainNumbers = []
        for a in arr:
            flag, num = check_and_getmainNum(a, default_pre, num_bit, drop_char=drop_char)
            check |= flag
            if flag:
                mainNumbers.append(num)
        return check, mainNumbers


def match(s1, s2, default_pre='Z', num_bit=5, drop_char=['.'], way='main_num') -> bool:
    ''' 判断字符串s1 和 s2 是否匹配
    :param s1: 片子病理号，s1只可能包含一个病理号
    :param s2: 临床或病理表的的病理号，s2可能有多个病理号
    :param default_pre: 病理号，缺省前缀
    :param num_bit: 编号位数限制
    :param drop_char: 需要除去的无效字符
    :param way: 匹配方式，main_num, 根据主号匹配      sub_num, 根据主号和副号匹配
    :return: 是否匹配，True or False
    '''
    if way == 'main_num':
        flag1, num1 = check_and_getmainNum(s1, default_pre=default_pre, num_bit=num_bit, drop_char=drop_char)
        flag2, nums2 = check_and_getmainNum_multi(s2, default_pre=default_pre, num_bit=num_bit, drop_char=drop_char)
        if flag1 and flag2 and (num1 in nums2):
            return True
        else:
            return False

    if way == 'sub_num':
        flag1, num1 = check_and_getsubNum(s1, default_pre=default_pre, num_bit=num_bit, drop_char=drop_char)
        flag2, num2 = check_and_getsubNum(s2, default_pre=default_pre, num_bit=num_bit, drop_char=drop_char)
        if flag1 and flag2 and (num1 == num2):
            return True
        else:
            return False


def load_data_excel(file_name, col_name=['病理号'], sheet_names=None):
    '''
    :param file_name: 待读取的文件名
    :param col_name: 读取的列名
    :param sheet_names: 读取的sheet名
    :return: 返回指定sheet，col_name的结果数据，会将多个sheet的结果合并到一起
    '''
    print("load data:", file_name)
    rdexcle = pd.read_excel(file_name, sheet_name=sheet_names, usecols=col_name)
    output = []
    for e in rdexcle:
        output += np.array((rdexcle[e])).tolist()
    return output


def pathologyNum_mapto_sickNum(file_names1=[], file_names2=[], default_pre='Z', num_bit=5, col_name1=['病理号'],
                               sheet_names1=None, col_name2=['患者代码', '病理编号'], sheet_names2=None, savedir='') -> List[
    List]:
    '''
    :param file_names1: 病理图编号的文件集合（含带副号的病理编号）
    :param file_names2: 临床表文件集合（含病理编号和患者代码）
    :param default_pre: 默认病理号前缀
    :param num_bit: 病理号编号部分的位数，默认5位
    :param col_name1: 文件集合1要读取的列的集合
    :param col_name2: 文件集合2要读取的列的集合
    :param savename: 映射结果的保存文件名，默认为pathology_mapto_sickno.csv， 第一列为：病理图的病理编号，第二列为：患者代码
    :param show_file_name: 是否显示文件名，用于表明当前数据的来源
    :return: 保存结果文件，output为[病理图编号,sickno,病理主号,是否匹配到]的格式的list
    '''
    input1 = []
    names1 = []
    input2 = []
    names2 = []
    for f1 in file_names1:
        f1_data = load_data_excel(f1, col_name=col_name1, sheet_names=sheet_names1)
        input1 += f1_data
        names1 += [os.path.basename(f1) for i in range(len(f1_data))]

    for f2 in file_names2:
        f2_data = load_data_excel(f2, col_name=col_name2, sheet_names=sheet_names2)
        input2 += f2_data
        names2 += [os.path.basename(f2) for i in range(len(f2_data))]

    print(len(input1), len(input2))

    output = []
    count = 0
    for i in tqdm(range(len(input1))):
        line1 = input1[i]
        s1 = line1[0]
        s1_file = names1[i]
        flag = False
        for j, line2 in enumerate(input2):
            s2 = line2[1]
            s2_file = names2[j]
            if match(s1, s2, default_pre, num_bit, way='main_num'):
                output += [[s1, line2[0], s2, True, s1_file, s2_file]]  # sickno: line2[0]
                count += 1
                if count % 500 == 0:
                    print(count)
                flag = True
                break
        if not flag:
            output += [[s1, None, None, False, None, None]]
    print(count)

    out_data = DataFrame(columns=['病理号', '患者代码', '病理编号', '是否匹配', '病理号所在文件', '患者代码和病理编号所在文件'])

    for i in tqdm(range(len(output))):
        out_data.loc[i] = output[i]

    # 保存文件
    savename = os.path.join(savedir, 'pNum_mapto_sickNum_' + str(datetime.date.today()) + '.xlsx')
    out_data.to_excel(savename)

    return output


def copy_tiles_file(source_dir, dist_dir, listfile: str, usecols=['病理号']):
    ''' 根据文件的list，将数据匹配的数据重一个文件从source_dir 拷贝到 dist_dir
    :param source_dir:
    :param dist_dir:
    :param listfile: 提供list的文件，支持csv和xlsx文件
    :param usecols:
    :return:
    '''
    if listfile.endswith('.csv'):
        list_pathology = pd.read_csv(listfile, usecols=usecols)
    elif listfile.endswith('.xlsx'):
        list_pathology = pd.read_excel(listfile, usecols=usecols)
    else:
        raise ValueError('参数listfile，只支持csv，xlsx文件')
    listdir_source = os.listdir(source_dir)
    list_pathology = np.array(list_pathology).flatten().tolist()

    count = 0
    count_null = 0
    for pathology in tqdm(list_pathology):
        if not isinstance(pathology, str):
            print('空病理号')
            count_null += 1
            continue

        for sub_dir in listdir_source:
            if os.path.exists(os.path.join(dist_dir, sub_dir)):
                count += 1
                continue
            if check_and_getsubNum(pathology) == check_and_getsubNum(sub_dir):
                print(sub_dir)
                shutil.copytree(os.path.join(source_dir, sub_dir), os.path.join(dist_dir, sub_dir))
                count += 1
    print('总数：', len(list_pathology), '成功拷贝：', count, '空病理号：', count_null, '其它：',
          len(list_pathology) - count - count_null)
