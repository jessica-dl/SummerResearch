"""
Main module of top down greedy anonymizaiton algorithm
"""
# @Article{Xu2006a,
#   Title = {Utility-based Anonymization for Privacy Preservation with Less Information Loss},
#   Author = {Xu, Jian and Wang, Wei and Pei, Jian and Wang, Xiaoyuan and Shi, Baile and Fu, Ada Wai-Chee},
#   Journal = {SIGKDD Explor. Newsl.},
#   Year = {2006},
#   Month = dec,
#   Number = {2},
#   Pages = {21--30},
#   Volume = {8},
#   Acmid = {1233324},
#   Address = {New York, NY, USA},
#   Doi = {10.1145/1233321.1233324},
#   ISSN = {1931-0145},
#   Issue_date = {December 2006},
#   Keywords = {data mining, k-anonymity, local recoding, privacy preservation, utility},
#   Numpages = {10},
#   Publisher = {ACM},
#   Url = {http://doi.acm.org/10.1145/1233321.1233324}
# }

# !/usr/bin/env python
# coding=utf-8

import pdb
from utils.utility import cmp_str, get_num_list_from_str
import operator
import random
import time


__DEBUG = False
QI_LEN = 5
GL_K = 0
RESULT = []
ATT_TREES = []
QI_RANGE = []
ROUNDS = 3


class Partition(object):

    """
    Class for Group, which is used to keep records
    Store tree node in instances.
    self.member: records in group
    self.middle: save the generalization result of this partition
    """

    def __init__(self, data, middle):
        """ Initialize with data and middle """
        
        self.can_split = True
        self.member = data[:]
        self.middle = middle[:]

    def __len__(self):
        """ return the number of records in partition """
        
        return len(self.member)

    def __str__(self):
        for mem in self.member:
            return str(mem)

def NCP(record):
    """ Compute Certainty Penalty of records """
    
    record_ncp = 0.0
    for i in range(QI_LEN):
        record_ncp += len(ATT_TREES[i][record[i]]) * 1.0 / QI_RANGE[i]
    return record_ncp


def NCP_dis(record1, record2):
    """ Use the NCP of generalization record1 and record2 as distance """
    
    mid = middle_record(record1, record2)
    return NCP(mid), mid


def NCP_dis_merge(partition, addition_set):
    """ Merge addition_set to current partition
        and update current partition.middle """
    
    mid = middle_group(addition_set)
    mid = middle_record(mid, partition.middle)
    return (len(addition_set) + len(partition)) * NCP(mid), mid


def NCP_dis_group(record, partition):
    """
    compute the NCP of record and partition
    """
    mid = middle_record(record, partition.middle)
    ncp = NCP(mid)
    return (1 + len(partition)) * ncp


def middle_record(record1, record2):
    """ Get the generalization result of record1 and record2"""
    
    mid = []
    for i in range(QI_LEN):
        mid.append(LCA(record1[i], record2[i], i))
    return mid


def middle_group(group_set):
    """ Get the generalization result of the group """
    
    len_group_set = len(group_set)
    mid = group_set[0]
    for i in range(1, len_group_set):
        mid = middle_record(mid, group_set[i])
    return mid


def LCA(u, v, index):
    """ Get lowest common ancestor of u, v from generalization hierarchy """
    
    gen_tree = ATT_TREES[index]
    # don't forget to add themselves (other the level will be higher)
    u_parent = list(gen_tree[u].parent)
    u_parent.insert(0, gen_tree[u])
    v_parent = list(gen_tree[v].parent)
    v_parent.insert(0, gen_tree[v])
    min_len = min(len(u_parent), len(v_parent))
    if min_len == 0:
        return '*'
    last = -1
    for i in range(min_len):
        pos = - 1 - i
        if u_parent[pos] != v_parent[pos]:
            break
        last = pos
    return u_parent[last].value


def get_pair(partition):
    """
    To get max distance pair in partition, we need O(n^2) running time.
    The author proposed a heuristic method: randomly pick u and get max_dis(u, v)
    with O(n) running time; then pick max(v, u2)...after run ROUNDS times.
    the dis(u, v) is nearly max.
    """
    len_partition = len(partition)
    for i in range(ROUNDS):
        if i == 0:
            u = random.randrange(len_partition)
        else:
            u = v
        max_dis = -1
        max_index = 0
        for i in range(len_partition):
            if i != u:
                rncp, _ = NCP_dis(partition.member[i], partition.member[u])
                if rncp > max_dis:
                    max_dis = rncp
                    max_index = i
        v = max_index
    return (u, v)


def distribute_record(u, v, partition):
    """ Distribute records based on NCP distance.
        Records will be assigned to nearer group. """
    
    record_u = partition.member[u][:]
    record_v = partition.member[v][:]
    u_partition = [record_u]
    v_partition = [record_v]
    remain_records = [item for index, item in enumerate(partition.member) if index not in set([u, v])]
    for record in remain_records:
        u_dis, _ = NCP_dis(record_u, record)
        v_dis, _ = NCP_dis(record_v, record)
        if u_dis > v_dis:
            v_partition.append(record)
        else:
            u_partition.append(record)
    return [Partition(u_partition, middle_group(u_partition)),
            Partition(v_partition, middle_group(v_partition))]


def balance(sub_partitions, index):
    """
    Two kinds of balance methods.
    1) Move some records from other groups
    2) Merge with nearest group
    The algorithm will choose one of them with minimal NCP
    index store the sub_partition with less than k records
    """
    
    less = sub_partitions.pop(index)
    more = sub_partitions.pop()
    all_length = len(less) + len(more)
    require = GL_K - len(less)
    # First method
    dist = {}
    for i, record in enumerate(more.member):
        dist[i], _ = NCP_dis(less.middle, record)

    sorted_dist = sorted(dist.iteritems(),
                         key=operator.itemgetter(1))
    nearest_index = [t[0] for t in sorted_dist[:require]]
    addition_set = [t for i, t in enumerate(more.member) if i in set(nearest_index)]
    remain_set = [t for i, t in enumerate(more.member) if i not in set(nearest_index)]
    first_ncp, first_mid = NCP_dis_merge(less, addition_set)
    r_middle = middle_group(remain_set)
    first_ncp += len(remain_set) * NCP(r_middle)
    # Second method
    second_ncp, second_mid = NCP_dis(less.middle, more.middle)
    second_ncp *= all_length
    if first_ncp <= second_ncp:
        less.member.extend(addition_set)
        less.middle = first_mid
        more.member = remain_set
        more.middle = r_middle
        sub_partitions.append(more)
    else:
        less.member.extend(more.member)
        less.middle = second_mid
        less.can_split = False
    sub_partitions.append(less)


def can_split(partition):
    """ Check if partition can be split any furthur """
    
    if partition.can_split is False:
        return False
    if len(partition) < 2 * GL_K:
        return False
    return True


def anonymize(partition):
    """
    Main procedure of top_down_greedy_anonymization.
    Recursively partition groups until it's no longer possible.
    """
    
    if can_split(partition) is False:
        RESULT.append(partition)      
        return 
    u, v = get_pair(partition)
    sub_partitions = distribute_record(u, v, partition)
    if len(sub_partitions[0]) < GL_K:
        balance(sub_partitions, 0)
    elif len(sub_partitions[1]) < GL_K:
        balance(sub_partitions, 1)
    p_sum = len(partition)
    c_sum = 0
    for sub_partition in sub_partitions:
        c_sum += len(sub_partition)
    if p_sum != c_sum:
        pdb.set_trace()
    for sub_partition in sub_partitions:
        anonymize(sub_partition)


def init(att_trees, data, k, QI_num=-1):
    """ Reset all global variables """
    
    global GL_K, RESULT, QI_LEN, ATT_TREES, QI_RANGE
    ATT_TREES = att_trees
    if QI_num <= 0:
        QI_LEN = len(data[0]) - 1
    else:
        QI_LEN = QI_num
    GL_K = k
    RESULT = []
    QI_RANGE = []


def Top_Down_Greedy_Anonymization(att_trees, data, k, QI_num=-1):
    """ Top Down Greedy Anonymization is a heuristic algorithm
        for relational dataset with numeric and categorical attbitues """
    
    init(att_trees, data, k, QI_num)
    result = []
    middle = []
    for i in range(QI_LEN):
        QI_RANGE.append(len(ATT_TREES[i]['*']))
        middle.append('*')
    whole_partition = Partition(data, middle)
    start_time = time.time()
    anonymize(whole_partition)
    rtime = float(time.time() - start_time)
    
    ncp = 0.0
    dp = 0.0
    for sub_partition in RESULT:
        rncp = 0.0
        gen_result = sub_partition.middle
        rncp = NCP(gen_result)
        for i in range(len(sub_partition)):
            result.append(gen_result[:])
        rncp *= len(sub_partition)
        dp += len(sub_partition) ** 2
        ncp += rncp
    # covert NCP to percentage
    ncp /= len(data)
    ncp /= QI_LEN
    ncp *= 100
    # ncp /= 10000
    if __DEBUG:
        from decimal import Decimal
        print "Discernability Penalty=%.2E" % Decimal(str(dp))
        print "K=%d" % k
        print "size of partitions"
        print len(RESULT)
        print[len(partition) for partition in RESULT]
        print "NCP = %.2f %%" % ncp
        print "Total running time = %.2f" % rtime
        # pdb.set_trace()
    return (result, (ncp, rtime))
