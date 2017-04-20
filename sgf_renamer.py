#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: felipem775
# Version: 0.1

import sys
import os
import binascii

def get_sgf_in_path(path):
    file_list = []
    for root, subdir, files in os.walk(path):
        for f in files:
            if f[-4:] == '.sgf' :
        		file_list.append(os.path.join(root,f))
    return file_list

def get_attributes(sgf_file):
    attribute_list = set(['GM','DT','PB','PW','BR','WR'])
    f = open(sgf_file,'r')
    lines = f.readlines()
    f.close()

    attributes = {}
    for l in lines:
        if l[0:2] in attribute_list:
            attributes[l[0:2]]=l[3:-2]
    return attributes

def get_crc32(filename):
    # http://www.matteomattei.com/how-to-calculate-the-crc32-of-a-file-in-python/
    buf = open(filename,'rb').read()
    buf = (binascii.crc32(buf) & 0xFFFFFFFF)
    return "%08X" % buf

if __name__ == "__main__":
    sgf_file_list = []
    try:
        sgf_file_list = get_sgf_in_path(sys.argv[1])
    except:
        print("ERROR Path doesn't exist")

    for sgf_file in sgf_file_list:
        attributes = get_attributes(sgf_file)
        crc32 = get_crc32(sgf_file)
        new_sgf_file = "{}/{}_{}[{}]_{}[{}]_[{}].sgf".format(os.path.dirname(sgf_file),attributes['DT'],attributes['PW'],attributes['WR'],attributes['PB'],attributes['BR'], crc32)
        try:
            os.rename(sgf_file,new_sgf_file)
        except:
            print("ERROR renaming {} to {}".format(sgf_file,new_sgf_file))
