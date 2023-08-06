# -*- coding: UTF-8 -*-
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from famCircle.bez import *
import sys

class Ks_allocation():
    def __init__(self, options):
        self.vertical = "False"
        self.model = "NG86"
        self.bins = "100"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readks(self):
        read_ks = []
        f = open(self.ks, 'r', encoding='utf-8')
        for row in f:
            if row[0] != '#' and row[0] != '\n':
                row = row.strip('\n').split('\t')
                if row[0] != 'id1' and len(row) != 2:
                    read_ks.append(row)
        kspd = pd.DataFrame(read_ks)
        kspd.rename(columns={0: 'id1', 1: 'id2',
                                2: 'ka_NG86', 3: 'ks_NG86',
                                4: 'ka_YN00', 5: 'ks_YN00'}, inplace=True)
        return kspd

    # 绘制核密度曲线图
    def KdePlot(self,x):
        # 绘制核密度分布直方图
        plt.figure(figsize=(20,10),dpi=1000)
        plt.grid(c='grey',ls='--',linewidth=0.2)
        sns.distplot(x,   # 指定绘图数据
                     kde=True,# 绘制密度曲线
                     bins=eval(self.bins),
                     vertical=eval(self.vertical),
                     kde_kws={'color': 'y', 'lw':0.3}, 
                     hist_kws={'color': 'c', 'alpha': 0.4})
        sns.kdeplot(data=x,color="lime", linewidth = 0.3, alpha = 0.5, 
                     shade=True,
                     vertical=eval(self.vertical),
                     bw_method =0.2,
                     bw_adjust = 0.2,
                     cut=0, 
                     label="KDE")
        plt.legend()
        plt.title('kernel density estimation')# 设置图片标题
        plt.xlabel('ks')# 设置 x 轴标签
        plt.ylabel('density')# 设置 y 轴标签

    def run(self):
        kspdx = self.readks()
        if self.model == "NG86":
            kspdx["ks_NG86"] = kspdx["ks_NG86"].astype(float)
            kspdx = kspdx[(kspdx["ks_NG86"] > 0) & (kspdx["ks_NG86"] < 99)]
            y = sorted(list(kspdx["ks_NG86"]))
        elif self.model == "YN00":
            kspdx["ks_YN00"] = kspdx["ks_YN00"].astype(float)
            kspdx = kspdx[(kspdx["ks_YN00"] > 0) & (kspdx["ks_YN00"] < 99)]
            y = sorted(list(kspdx["ks_YN00"]))
        self.KdePlot(y)
        plt.savefig(self.savefile)# 存储图片
        sys.exit(0)
