"""
utility functions
"""
# !/usr/bin/env python
# coding=utf-8


def cmp_str(element1, element2):
    """compare number in str format correctley
    """
    try:
        return ((element1 > element2) - (element1 < element2)) # return cmp(int(element1), int(element2))
    except ValueError:
        ((element1 > element2) - (element1 < element2))


def get_num_list_from_str(stemp):
    """
    if float(stemp) works, return [stemp]
    else return, stemp.split(',')

    """
    try:
        float(stemp)
        return [stemp]
    except ValueError:
        return stemp.split(',')
