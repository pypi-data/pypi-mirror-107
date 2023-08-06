# -*- coding: utf-8 -*-
# @Time     : 2021/4/26 18:16
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : cutImg.py
# @info     :


import os

# os.add_dll_directory('D:\Anaconda3\Library\openslide-win64-20171122\\bin')  # 添加自己的openslide动态库的文件路径
# os.add_dll_directory('D:\Anaconda3\Library\openslide-win64-20171122\\lib')  # 添加自己的openslide动态库的文件路径

##########################################################################################################################
# os.environ['PATH'] = 'D:\Anaconda3\Library\openslide-win64-20171122\\bin'+';'+os.environ['PATH']   in lowlevel.py      #
#                                                                                                                        #
##########################################################################################################################

import numpy as np
import openslide
import pandas as pd
from PIL import Image
from tqdm import tqdm
import shutil
from typing import List

from ufy.core.utils.tools import energy,find_file

def cut_img_energy(img_file, todir, file_format=['mrxs', 'tiff', 'ndpi'], energy_threshold=0.6, start_k=0, end_k=0,
                   cut_size=(2000, 2000), overlap=(0, 0), issave=False, max_level=4):
    ''' 切图，并按能量值排序
    :param img_file: 图片文件
    :param todir: 保存路径
    :param file_format: 默认支持'mrxs','tiff','npdi'格式的图片
    :param energy_threshold:能量阈值
    :param K: 取文件个数
    :param cut_size: 切图尺寸
    :param overlap: 重叠像素，默认不重叠
    :param issave: 是否保存图片，默认不保存
    :param max_level: 最大图层数，默认值为：4
    :return: count 切图并筛选的个数
    '''
    cut_size = np.array(cut_size).astype(int)
    overlap = np.array(overlap).astype(int)
    if start_k > end_k:
        print('输入必须满足：start_k < end_k')
    if os.path.basename(img_file).split('.')[-1] not in file_format:
        print('不支持该格式的文件，请检查文件格式！！！')
        print('目前支持的文件格式有：', file_format)
        return 0

    # open image
    try:
        source = openslide.open_slide(img_file)
    except:
        print("XXXXXX 不能打开文件：" + img_file)
        return 0

    level_count = source.level_count
    if level_count > max_level:
        LEVEL = max_level
    else:
        LEVEL = level_count - 1

    if (LEVEL < max_level):
        times = 2 ** LEVEL
        TILESIZE = cut_size // times
    else:
        times = 2 ** max_level
        TILESIZE = cut_size // times

    print(img_file + " 总计有:" + str(source.level_count) + "层")

    try:
        img = np.array(source.read_region((0, 0), LEVEL, source.level_dimensions[LEVEL]).convert('RGB'))
    except:
        print("XXXXXX 不能打开文件-：" + img_file)
        return 0

    eng = energy(img)
    w, h = eng.shape
    num_pixes = TILESIZE[0] * TILESIZE[0]

    # ROI grid
    grid = []
    power = []
    count = 0
    for i in np.arange((w - overlap[0]) // (TILESIZE[0] - overlap[0])):
        x = i * (TILESIZE[0] - overlap[0])
        for j in np.arange((h - overlap[1]) // (TILESIZE[1] - overlap[1])):
            y = j * (TILESIZE[1] - overlap[1])
            tile_eng = eng[x:(x + TILESIZE[0]), y:(y + TILESIZE[1])].copy()
            tile_power = np.sum(tile_eng) / num_pixes
            power.append(tile_power)
            grid.append([x, y])

    power_grid = pd.DataFrame({'power': power, 'grid': grid})
    power_grid = power_grid.sort_values(by='power', ascending=False)
    if not os.path.exists(todir):
        os.makedirs(todir)
    if energy_threshold == 0:
        try:
            with tqdm(range(start_k, end_k + 1, 1)) as t:
                for i in t:
                    if i < len(power_grid):
                        count += 1
                        if issave:
                            loc = power_grid.iloc[i]
                            x = loc['grid'][0] * times
                            y = loc['grid'][1] * times
                            filename = todir + '/' + str(i + 1) + '__' + np.str(x) + '_' + np.str(y) + '.jpg'
                            image = np.array(source.read_region((y, x), 0, (2000, 2000)))  # (shape : 2000,2000,4)
                            image = Image.fromarray(image).convert(mode='RGB')
                            image.save(filename)
        except:
            t.close()
            raise
        t.close()
        return count
    else:
        try:
            with tqdm(range(len(power_grid))) as t:
                for i in t:
                    loc = power_grid.iloc[i]
                    energy_tile = loc['power']
                    if energy_tile > energy_threshold:
                        count += 1
                        if issave:
                            x = loc['grid'][0] * times
                            y = loc['grid'][1] * times
                            filename = todir + '/' + str(i + 1) + '__' + np.str(x) + '_' + np.str(y) + '.jpg'
                            image = np.array(source.read_region((y, x), 0, size=cut_size))  # (shape : 2000,2000,4)
                            image = Image.fromarray(image).convert(mode='RGB')
                            image.save(filename)
                    else:
                        break
        except KeyboardInterrupt:
            t.close()
            raise
        t.close()
        return count


def cut_img_dir(dir_source='', todir_pre='', file_format=['mrxs', 'tiff', 'ndpi'], energy_threshold=0.6, start_k=0,
                end_k=0, cut_size=(2000, 2000), overlap=(0, 0), issave=False, max_level=4):
    '''
    :param dir_source:
    :param todir_pre:
    :param file_format:
    :param energy_threshold:
    :param start_k:
    :param end_k:
    :param cut_size:
    :param overlap:
    :param issave:
    :param max_level:
    :return:
    '''

    temp_dir = '../data/temp/'  # 临时文件夹
    img_files = find_file(dir_source=dir_source, file_format=file_format)
    print('图片文件数：', len(img_files))

    count = 0
    for img_file in img_files:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        if not copy_file_to_tempdir(filename=img_file, copydir_format=['mrxs'], temp_dir=temp_dir):
            continue
        todir = make_todir(filename=img_file, todir_pre=todir_pre, dir_pre=dir_source)
        count += cut_img_energy(img_file, todir=todir, file_format=file_format,
                                energy_threshold=energy_threshold, cut_size=cut_size, overlap=overlap,
                                issave=issave, max_level=max_level, start_k=start_k, end_k=end_k)
        shutil.rmtree(temp_dir)
    print('tiles 总数：', count)
    return count


def copy_file_to_tempdir(filename: str, copydir_format: List[str] = ['mrxs'], temp_dir: str = 'data/temp/') -> bool:
    '''
    :param filename: 待copy的文件名
    :param copydir_format: 需要copy文件夹的文件格式
    :param temp_dir: 临时保存的文件夹
    :return: 返回bool值，表示是copy成功
    '''
    shutil.copyfile(filename, temp_dir + os.path.basename(filename))
    filetype = os.path.basename(filename).split('.')[-1]
    if filetype in copydir_format:
        f_dir = filename.replace(filetype, '')
        if not os.path.exists(f_dir):
            print(filename, '缺少相关文件！！！')
            return False
        flist = os.listdir(f_dir)
        temp_dir2 = os.path.join(temp_dir, os.path.basename(filename).split('.')[0] + '/')
        if not os.path.exists(temp_dir2):
            os.makedirs(temp_dir2)
        for f_ in flist:
            shutil.copyfile(os.path.join(f_dir, f_), temp_dir2 + os.path.basename(f_))
    return True


def make_todir(filename: str, dir_pre: str, todir_pre: str) -> str:
    '''
    :param filename: 文件名
    :param dir_pre: 文件名前缀，用于去掉无用前缀(共同目录部分)
    :param todir_pre: todir的根目录
    :return:
    '''
    f = filename.replace(dir_pre, '')  # 去掉文件路径无用的头信息
    todir_tail = f.split('.')[0] + '/'  # 保存子子文件夹的名字
    todir = os.path.join(todir_pre, todir_tail)
    try:
        if not os.path.isdir(todir):
            os.makedirs(todir)
    except:
        print('创建文件夹失败！')
    return todir


if __name__ == '__main__':
    # cut_img_dir(dir_source="K:\\raw-slices\\huaxi-raw slices\\12\\12-raw slices\\12  HE-3d\\zz4-无癌\\", todir_pre='L:/12-normal-tiles/', file_format=['mrxs', 'tiff', 'npdi'],
    #             issave=True, start_k=100, end_k=600, energy_threshold=0)
    # cut_img_dir(dir_source="../data/original_dir/", todir_pre='../data/test/', file_format=['mrxs', 'tiff', 'npdi'],
    #             issave=True, start_k=100, end_k=600, energy_threshold=0)
    cut_img_dir(dir_source="E:\OneDrive\\rebar\一期善后\stitich\\", todir_pre='../data/test/',
                file_format=['mrxs', 'tiff', 'npdi', 'bmp'],
                issave=True, start_k=0, end_k=600, energy_threshold=0, overlap=(500, 500))
