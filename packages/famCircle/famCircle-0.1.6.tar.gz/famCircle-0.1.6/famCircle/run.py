# -*- coding: UTF-8 -*-
import argparse
import os
import sys
import configparser
import pandas as pd
import famCircle
import famCircle.bez as bez
from famCircle.hmmer import hmmer
from famCircle.screen import screen
from famCircle.Ks_allocation import Ks_allocation
from famCircle.Ks_block import Ks_block
from famCircle.circle import circle
from famCircle.circle_all import circle_all
from famCircle.outer import outer
from famCircle.inner import inner
from famCircle.typing import typing

parser = argparse.ArgumentParser(
    prog = 'famCircle', usage = '%(prog)s [options]', epilog = "", formatter_class = argparse.RawDescriptionHelpFormatter,)
parser.description = '''\
圈图构建
    -------------------------------------- '''
parser.add_argument("-v", "--version", action = 'version', version='0.1.6')
parser.add_argument("-hmm", dest = "hmmer",
                    help = "基因家族鉴定")
parser.add_argument("-s", dest = "screen",
                    help = "结构域数量与分布")
parser.add_argument("-ks", dest = "Ks_allocation",
                    help = "gene_Ks可视化")
parser.add_argument("-kb", dest = "Ks_block",
                    help = "block_Ks可视化")
parser.add_argument("-t", dest = "typing",
                    help = "结构域数据标准化")
parser.add_argument("-c", dest = "circle",
                    help = "共线性可视化")
parser.add_argument("-ca", dest = "circle_all",
                    help = "blast可视化")
parser.add_argument("-o", dest = "outer",
                    help = "当基因组复杂且重复基因多时在圈图外围显示，构建发射状基因圈图")
parser.add_argument("-i", dest = "inner",
                    help = "当基因组简单且重复基因比较少时在圈图内显示，构建内卷状基因圈图")

args = parser.parse_args()

def run_hmmer():
    options = bez.load_conf(args.hmmer, 'hmmer')
    hmmer1 = hmmer(options)
    hmmer1.run()

def run_screen():
    options = bez.load_conf(args.screen, 'screen')
    screen1 = screen(options)
    screen1.run()

def run_Ks_allocation():
    options = bez.load_conf(args.Ks_allocation, 'Ks_allocation')
    lookKs1 = Ks_allocation(options)
    lookKs1.run()

def run_Ks_block():
    options = bez.load_conf(args.Ks_block, 'Ks_block')
    lookKs0 = Ks_block(options)
    lookKs0.run()

def run_typing():
    options = bez.load_conf(args.typing, 'typing')
    typing1 = typing(options)
    typing1.run()

def run_circle():
    options = bez.load_conf(args.circle, 'circle')
    circle1 = circle(options)
    circle1.run()

def run_circle_all():
    options = bez.load_conf(args.circle_all, 'circle_all')
    circle0 = circle_all(options)
    circle0.run()

def run_outer():
    options = bez.load_conf(args.outer, 'outer')
    outer1 = outer(options)
    outer1.run()

def run_inner():
    options = bez.load_conf(args.inner, 'inner')
    inner1 = inner(options)
    inner1.run()

def module_to_run(argument):
    switcher = {
        'hmmer': run_hmmer,
        'screen': run_screen,
        'Ks_allocation': run_Ks_allocation,
        'Ks_block': run_Ks_block,
        'typing': run_typing,
        'circle': run_circle,
        'circle_all': run_circle_all,
        'outer': run_outer,
        'inner': run_inner,
    }
    return switcher.get(argument)()

def main():
    path = famCircle.__path__[0]
    options = {
               'hmmer': 'hmmer.conf',
               'screen': 'screen.conf',
               'Ks_allocation': 'Ks_allocation.conf',
               'Ks_block': 'Ks_block.conf',
               'typing': 'typing.conf',
               'circle': 'circle.conf',
               'circle_all': 'circle_all.conf',
               'outer': 'outer.conf',
               'inner': 'inner.conf',
               }
    for arg in vars(args):
        value = getattr(args, arg)
        # print(value)
        if value is not None:
            if value in ['?', 'help', 'example']:
                f = open(os.path.join(path, 'example', options[arg]))
                print(f.read())
            elif value == 'e':
                out = '''\
        File example
        [fpchrolen]
        chromosomes number_of_bases
        *   *
        *   *
        *   *
        [fpgff]
        chromosomes gene    start   end
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [fpgenefamilyinf]
        gene1   gene2   Ka  Ks
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [alphagenepairs]
        gene1   gene2
        *   *   *
        *   *   *
        *   *   *

        The file columns are separated by Tab
        -----------------------------------------------------------    '''
                print(out)
            elif not os.path.exists(value):
                print(value+' not exits')
                sys.exit(0)
            else:
                module_to_run(arg)

