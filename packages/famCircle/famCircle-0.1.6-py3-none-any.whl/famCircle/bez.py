# -*- coding: UTF-8 -*-
import configparser
import os
import re
import famCircle
import numpy as np
import pandas as pd
from Bio import Seq, SeqIO, SeqRecord
import codecs
# Bezier functions

def config():
    conf = configparser.ConfigParser()
    conf.read(os.path.join(famCircle.__path__[0], 'conf.ini'))
    return conf.items('ini')

def load_conf(file, section):
    conf = configparser.ConfigParser()
    conf.read(file)
    return conf.items(section)

def calculate_coef(p0, p1, p2, p3):
    c = 3*(p1 - p0)
    b = 3*(p2 - p1) -c
    a = p3 - p0 - c - b
    return c, b, a

def Bezier(plist, t):
    # p0 : origin, p1, p2 :control, p3: destination
    p0, p1, p2, p3 = plist
    # calculates the coefficient values
    c, b, a = calculate_coef(p0, p1, p2, p3)
    tsquared = t**2
    tcubic = tsquared*t
    return a*tcubic + b*tsquared + c*t + p0

def gene_length(gfffile):
    # 读取基因长度，得到平均长度和最小最大长度
    f = open(gfffile,'r', encoding='utf-8')
    genelength = {}
    for row in f:
        if row[0] != '\n' and row[0] != '#':
            row = row.strip('\n').split('\t')
            if str(row[1]) in genelength.keys():
                continue
            if 'chr' == str(row[1])[3:6]:
                continue
            length = abs(int(row[3]) - int(row[2]))
            genelength[str(row[1])] = length
    f.close()
    lt = []
    for i in genelength.values():
        lt.append(i)
    pj = sum(lt)/len(lt)
    return pj