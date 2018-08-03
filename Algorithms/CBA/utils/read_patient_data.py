"""
read patient data
"""

#!/usr/bin/env python
# coding=utf-8

from models.gentree import GenTree
from utils.utility import cmp_str
import pdb

FILE_NAME = "patient"
ATT_NAMES = ['age', 'postal_codes', 'province', 'diagnosis', 'medication']

QI_INDEX = [0, 1, 2, 3, 4]

SA_INDEX = -1

__DEBUG = False


def read_tree():
    """
    read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    for i in range(len(att_names)):
        att_trees.append(read_tree_file(att_names[i]))
    return att_trees


def read_tree_file(treename):
    """
    read tree data from treename
    """
    leaf_to_path = {}
    att_tree = {}
    prefix = "data/" + FILE_NAME + "_"
    suffix = ".txt"
    with open (prefix + treename + suffix, 'r') as treefile:
        att_tree['*'] = GenTree('*')
        if __DEBUG:
            print "Reading Tree" + treename
        for line in treefile:
            # delete \n
            if len(line) <= 1:
                print "Line too short"
                break
            line = line.strip()
            temp = line.split(';')
            # copy temp
            temp.reverse()
            for i, t in enumerate(temp):
                isleaf = False
                if i == len(temp) - 1:
                    isleaf = True
                # try and except is more efficient than 'in'
                try:
                    att_tree[t]
                except:
                    att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    if __DEBUG:
        print "Nodes No. = %d" % att_tree['*'].support
    treefile.close()
    return att_tree


def read_data():
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    # oder categorical attributes in intuitive order
    # here, we use the appear number
    data_file = open('data/' + FILE_NAME + '.data', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        if len(line) == 0 or '?' in line:
            continue
        # remove double spaces
        line = line.replace(' ', '')
        temp = line.split(',')
        ltemp = []
        for i in range(QI_num):
            index = QI_INDEX[i]
            ltemp.append(temp[index])
        ltemp.append(temp[SA_INDEX])
        data.append(ltemp)

    return data
