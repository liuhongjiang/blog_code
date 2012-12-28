#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SMO的一个简单实现
# implement SMO

import sys
import math
import matplotlib.pyplot as plt

samples = []
labels = []
class svm_params:
    def __init__(self):
        self.a = []
        self.b = 0

params = svm_params()
e_dict = []

#train_data = "svm.train_mix_ok"
train_data = "svm.train"

def loaddata():
    fn = open(train_data,"r")
    for line in fn:
        line = line[:-1]
        vlist = line.split("\t")
        samples.append((int(vlist[0]), int(vlist[1])))
        labels.append(int(vlist[2]))
        params.a.append(0.0)
    fn.close()

# linear
def kernel(j, i):
    ret = 0.0
    for idx in range(len(samples[j])):
        ret += samples[j][idx] * samples[i][idx]
    return ret

def predict_real_diff(i):
    diff = 0.0
    for j in range(len(samples)):
        diff += params.a[j] * labels[j] * kernel(j,i)
    diff = diff + params.b - labels[i]
    return diff

def init_e_dict():
    for i in range(len(params.a)):
        e_dict.append(predict_real_diff(i))

def update_e_dict():
    for i in range(len(params.a)):
        e_dict[i] = predict_real_diff(i)

def train(tolerance, times, C):
    time = 0
    init_e_dict()
    updated = True
    while time < times and updated:
        updated = False
        time += 1
        for i in range(len(params.a)):
            ai = params.a[i]
            Ei = e_dict[i]
            # 违反KKT
            # agaist the KKT
            if (labels[i] * Ei < -tolerance and ai < C) or (labels[i] * Ei > tolerance and ai > 0):
                for j in range(len(params.a)):
                    if j == i: continue
                    eta = kernel(i, i) + kernel(j, j) - 2 * kernel(i, j)
                    if eta <= 0:
                        continue
                    new_aj = params.a[j] + labels[j] * (e_dict[i] - e_dict[j]) / eta 
                    L = 0.0
                    H = 0.0
                    if labels[i] == labels[j]:
                        L = max(0, params.a[j] + params.a[i] - C)
                        H = min(C, params.a[j] + params.a[i])
                    else:
                        L = max(0, params.a[j] - params.a[i]) 
                        H = min(C, C + params.a[j] - params.a[i])
                    if new_aj > H:
                        new_aj = H
                    if new_aj < L:
                        new_aj = L
                    # 《统计学习方法》公式7.109（下同）
                    # formula 7.109
                    new_ai = params.a[i] + labels[i] * labels[j] * (params.a[j] - new_aj)

                    # 第二个变量下降是否达到最小步长
                    # decline enough for new_aj
                    if abs(params.a[j] - new_aj) < 0.001:
                        print "j = %d, is not moving enough" % j
                        continue

                    # formula 7.115
                    new_b1 = params.b - e_dict[i] - labels[i]*kernel(i,i)*(new_ai-params.a[i]) - labels[j]*kernel(j,i)*(new_aj-params.a[j]) 
                    # formula 7.116
                    new_b2 = params.b - e_dict[j] - labels[i]*kernel(i,j)*(new_ai-params.a[i]) - labels[j]*kernel(j,j)*(new_aj-params.a[j]) 
                    if new_ai > 0 and new_ai < C: new_b = new_b1
                    elif new_aj > 0 and new_aj < C: new_b = new_b2
                    else: new_b = (new_b1 + new_b2) / 2.0
                    
                    params.a[i] = new_ai
                    params.a[j] = new_aj
                    params.b = new_b
                    update_e_dict()
                    updated = True
                    print "iterate: %d, changepair: i: %d, j:%d" %(time, i, j)

def draw(tolerance, C):
    plt.xlabel(u"x1")
    plt.xlim(0, 100)
    plt.ylabel(u"x2")
    plt.ylim(0, 100)
    plt.title("SVM - %s, tolerance %f, C %f" % (train_data, tolerance, C))
    ftrain = open(train_data, "r")
    for line in ftrain:
        line = line[:-1]
        sam = line.split("\t")
        if int(sam[2]) > 0:
            plt.plot(sam[0],sam[1], 'or')
        else:
            plt.plot(sam[0],sam[1], 'og')
    
    w1 = 0.0 
    w2 = 0.0
    for i in range(len(labels)):
        w1 += params.a[i] * labels[i] * samples[i][0]
        w2 += params.a[i] * labels[i] * samples[i][1]
    w = - w1 / w2

    b = - params.b / w2
    r = 1 / w2

    lp_x1 = [10, 90]
    lp_x2 = []
    lp_x2up = []
    lp_x2down = []
    for x1 in lp_x1:
        lp_x2.append(w * x1 + b)
        lp_x2up.append(w * x1 + b + r)
        lp_x2down.append(w * x1 + b - r)
    plt.plot(lp_x1, lp_x2, 'b')
    plt.plot(lp_x1, lp_x2up, 'b--')
    plt.plot(lp_x1, lp_x2down, 'b--')
    plt.show()

if __name__ == "__main__":
    loaddata()
    print samples
    print labels
    # 惩罚系数
    # penalty for mis classify
    C = 10
    # 计算精度
    # computational accuracy 
    tolerance = 0.0001
    train(tolerance, 100, C)
    print "a = ", params.a
    print "b = ", params.b
    support =  []
    for i in range(len(params.a)):
        if params.a[i] > 0 and params.a[i] < C:
            support.append(samples[i])
    print "support vector = ", support
    draw(tolerance, C)
