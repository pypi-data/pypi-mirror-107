import os

from PIL import Image
import numpy as np
from scipy import ndimage as ndi
import cv2
from typing import List


def energy(img, savename='energy.jpg', issave=False):
    """
        Simple gradient magnitude energy map.
    """
    xgrad = ndi.convolve1d(img, np.array([1, 0, -1]), axis=1, mode='wrap')
    ygrad = ndi.convolve1d(img, np.array([1, 0, -1]), axis=0, mode='wrap')

    grad_mag = np.sqrt(np.sum(xgrad ** 2, axis=2) + np.sum(ygrad ** 2, axis=2))

    if issave:
        # cv2.imwrite(savename, grad_mag.astype(np.uint8))
        image = Image.fromarray(grad_mag.astype(np.uint8))
        image.save(savename)
    return grad_mag


def find_file(dir_source: str, file_format: List[str]) -> List[str]:
    ''' 在源文件夹，递归搜索file_format 格式的文件，并用file_list返回
    :param dir_source: 源文件夹
    :param file_format: 需要搜索的文件格式
    :return: 返回符合格式的文件的列表：file_list
    '''
    dirlist = os.listdir(dir_source)

    file_list = []
    for f in dirlist:
        f = os.path.join(dir_source, f)
        if os.path.isdir(f):
            file_list += find_file(f, file_format)
        elif str.lower(os.path.basename(f).split('.')[-1]) in file_format:
            file_list.append(f)
    return file_list


if __name__ == '__main__':
    # alllist = []
    alllist = find_file("E:/OneDrive/rebar/一期善后/stitich", file_format=['json'])
    print(alllist)
