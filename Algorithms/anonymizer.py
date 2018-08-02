"""
run top_down_greedy_anonymization with given argv
"""

# !/usr/bin/env python
# coding=utf-8
from top_down_greedy_anonymization import Top_Down_Greedy_Anonymization
from utils.read_adult_data import read_data as read_adult
from utils.read_adult_data import read_tree as read_adult_tree
from utils.read_adult_data import FILE_NAME as ADULT_FILE

from utils.read_informs_data import read_data as read_informs
from utils.read_informs_data import read_tree as read_informs_tree

from utils.read_patient_data import read_data as read_patient
from utils.read_patient_data import read_tree as read_patient_tree
from utils.read_patient_data import FILE_NAME as PATIENT_FILE

import sys, copy, random
import pdb

global K_CONST
K_CONST = 2

DATA_SELECT = 'a'


def get_result_one(att_trees, data, K_CONST):
    """ Run Top_Down_Greedy_Anonymization once, with k=10 """

    print "K=%d" % K_CONST
    result, eval_result = Top_Down_Greedy_Anonymization(att_trees, data, K_CONST)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + "seconds"


def get_result_k(att_trees, data):
    """ Change K, while fixing QD and size of dataset """
    
    data_back = copy.deepcopy(data)
    # for K in range(5, 105, 5):
    for k in [2, 5, 10, 25, 50, 100]:
        print '#' * 30
        print "K=%d" % k
        result, eval_result = Top_Down_Greedy_Anonymization(att_trees, data, k)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + "seconds"

def get_result_dataset(att_trees, data, FILE_NAME, K_CONST, n=10):
    """ Fix k and QI, while changing size of dataset
        n is the proportion number. """
    # what is a proportion number
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % K_CONST
    joint = length / 6
    h = 6
    if joint == 1:
        h
##    elif length % joint == 0:
##        h += 1
    pos = (h) * joint
    ncp = rtime = 0
 
    print '#' * 30
    print "Size of dataset %d" % pos
    
    for j in range(n):
        
        temp = random.sample(data, pos) # chooses pos number of elements from data
        result, eval_result = Top_Down_Greedy_Anonymization(att_trees, temp, K_CONST)
        ncp += eval_result[0]
        rtime += eval_result[1]
        data = copy.deepcopy(data_back)   
        result_file = FILE_NAME + "_resultfile.csv"
        
        with open(result_file, "w") as rf:
            for r in result:
                outstring = ""
                sepBy = ","
                for val in r:
                    outstring += val
                    outstring += sepBy
                    
                rf.write(outstring)
                rf.write("\n")
                    
    ncp /= n
    rtime /= n
    print "Average NCP %0.2f" % ncp + "%"
    print "Running time %0.2f" % rtime + "seconds"
    print '#' * 30

##def get_result_dataset(att_trees, data, FILE_NAME, K_CONST, n=10):
##    """ Fix k and QI, while changing size of dataset
##        n is the proportion number.
##        This version of get_result_dataset """
##    # what is a proportion number
##    # what is joint and why is it 5000?
##    
##    data_back = copy.deepcopy(data)
##    length = len(data_back)
##    print "K=%d" % K_CONST
##    joint = 5000
##    h = length / joint
##    if length % joint == 0:
##        h += 1
##    for i in range(1, h + 1):
##        pos = i * joint
##        ncp = rtime = 0
##        if pos > length:
##            continue
##        print '#' * 30
##        print "Size of dataset %d" % pos
##        for j in range(n):
##            temp = random.sample(data, pos)
##            result, eval_result = Top_Down_Greedy_Anonymization(att_trees, temp, K_CONST)
##            ncp += eval_result[0]
##            rtime += eval_result[1]
##            data = copy.deepcopy(data_back)
##
##            result_file = FILE_NAME + "_resultfile.csv"
##            with open(result_file, "w") as rf:
##                for r in result:
##                    outstring = ""
##                    sepBy = ","
##                    for val in r:
##                        outstring += val
##                        outstring += sepBy
##                        
##                    rf.write(outstring)
##                    rf.write("\n")
##                    
##        ncp /= n
##        rtime /= n
##        print "Average NCP %0.2f" % ncp + "%"
##        print "Running time %0.2f" % rtime + "seconds"
##        print '#' * 30


def get_result_qi(att_trees, data, K_CONST):
    """ Change number of QIs, while fixing K and size of dataset """
    
    data_back = copy.deepcopy(data)
    ls = len(data[0])
    for i in reversed(range(1, ls)):
        print '#' * 30
        print "Number of QI=%d" % i
        result, eval_result = Top_Down_Greedy_Anonymization(att_trees, data, K_CONST, i)
        data = copy.deepcopy(data_back)
        print "NCP %0.2f" % eval_result[0] + "%"
        print "Running time %0.2f" % eval_result[1] + "seconds"


if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        DATA_SELECT = sys.argv[1]
        FLAG = sys.argv[2]
    except: 
        pass
    INPUT_K = 10
    # read record
    if DATA_SELECT == 'i':
        print "INFORMS data"
        DATA = read_informs()
        ATT_TREES = read_informs_tree()
        FILE_NAME = INFORMS_FILE
    elif DATA_SELECT == "p":
        print "PATIENT data"
        DATA = read_patient()
        ATT_TREES = read_patient_tree()
        FILE_NAME = PATIENT_FILE
    else:
        print "ADULT data"
        DATA = read_adult()
        ATT_TREES = read_adult_tree()
        FILE_NAME = ADULT_FILE
    if FLAG == 'k':
        get_result_k(ATT_TREES, DATA)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, DATA, K_CONST)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA, FILE_NAME, K_CONST)
    elif FLAG == '':
        get_result_one(ATT_TREES, DATA, K_CONST)
    else:
        try:
            INPUT_K = int(FLAG)
            res = get_result_one(DATA, INPUT_K)
        except ValueError:
            print "Usage: python anonymizer [a | i | p] [k | qi | data]"
            print "a: ADULT dataset, i: INFORMS dataset, p: PATIENT dataset"
            print "k: varying k"
            print "qi: varying qi numbers"
            print "data: varying size of dataset"
            print "example: python anonymizer a 10"
            print "example: python anonymizer a k"
            
    # anonymized dataset is stored in result
    get_result_dataset(ATT_TREES, DATA, FILE_NAME, K_CONST)
    
