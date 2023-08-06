# -*- coding: utf-8 -*-
# @Time     : 2021/5/8 23:17
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : BinTree.py
# @info     :

class BiTreeNode:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class BinTree:
    def __init__(self, rootval):
        self.root = BiTreeNode(rootval)
        pass

    def add(self, value, parent: BiTreeNode, child):
        if child == 'left':
            parent.left = BiTreeNode(value)
        elif child == 'right':
            parent.right = BiTreeNode(value)
        else:
            raise ValueError('指定孩子类型有误!!!,二叉树只有left,right两种孩子类型，没有'+child+'类型')


    def remove(self, node: BiTreeNode):
        pass

    def traverse(self, way: str = 'prior_recursive'):
        pass

    def __traverse_prior__(self):
        '''
        :return:
        '''
        pass

if __name__ == '__main__':
    bitree = BinTree(0)
    bitree.add(1,bitree.root,'left')
