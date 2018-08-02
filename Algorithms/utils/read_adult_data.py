"""
read adult data
"""

#!/usr/bin/env python
# coding=utf-8

# Read data and read tree fuctions for INFORMS data
# attributes ['age', 'workclass', 'final_weight', 'education', 'education_num', 'matrital_status', 'occupation',
# 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'class']
# QID ['age', 'workcalss', 'education', 'matrital_status', 'race', 'sex', 'native_country']
# SA ['occopation']
from models.gentree import GenTree
from utils.utility import cmp_str
import pdb

FILE_NAME = "adult"
ATT_NAMES = ['age', 'workclass', 'final_weight', 'education',
             'education_num', 'marital_status', 'occupation', 'relationship',
             'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
             'native_country', 'class']
""" 9 attributes are used as QI attributes
    age, workclass, education, marital_status, occupation, relationship,
    race, sex, native_country """

QI_INDEX = [0, 1, 3, 5, 6, 7, 8, 9, 13]

SA_INDEX = -1

__DEBUG = False


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
    data_file = open('data/' + FILE_NAME + '.data', 'r')
    for line in data_file:
        line = line.strip()
        # remove empty and incomplete lines
        # only 30162 records will be kept
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
    postfix = ".txt"
    with open (prefix + treename + postfix, 'r') as treefile:
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
