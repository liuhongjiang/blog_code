#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pegasos implemented in Python

import os
import sys
import math

G_WEIGHT = []

def parse_image(path):
    img_map = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-2]
        for ch in line:
            img_map.append(int(ch))
    return img_map

def predict(model, data):
    ret = 0
    for i in range(32*32):
        ret += model[i]*data[i]
    return ret

def train_one_model(data, label, sampleNum, modelNum):
    pvalue = predict(G_WEIGHT[modelNum], data)
    # the hinge loss
    if pvalue * label >= 1:
        return
    
    # update model
    lambd = 0.5
    new_weight = []
    for i in range(32*32):
        # pegasos
        a = G_WEIGHT[modelNum][i] * ( 1 - 1.0/sampleNum) + (1.0 / (lambd * sampleNum))*label*data[i]
        new_weight.append(a)

    # projection
    norm2 = 0
    for i in range(32*32):
        norm2 += math.pow(new_weight[i], 2)
    norm2 = math.sqrt(norm2)
    if norm2 > (1/math.sqrt(lambd)):
        for i in range(32*32): 
            G_WEIGHT[modelNum][i] = new_weight[i]/(norm2 * math.sqrt(lambd)) 
    else:
        G_WEIGHT[modelNum] = new_weight

def train_one_sample(data, num, sampleNum):
    for modelNum in range(10):
        label = -1
        if num == modelNum:
            label = 1
        train_one_model(data, label, sampleNum, modelNum)

if __name__== "__main__":
    for i in range(10):
        G_WEIGHT.append([])
        for j in range(32 * 32):
            G_WEIGHT[i].append(0)

    dirpath = "./trainingDigits/"
    files = os.listdir(dirpath)
    sampleNum = 0
    for file in files:
        print "training:", file
        data = parse_image(dirpath + file)
        num = int(file[0])
        sampleNum += 1
        train_one_sample(data, num, sampleNum)

    # test
    testdir = "./testDigits/"
    files = os.listdir(testdir)  
    right = 0
    wrong = 0
    can_not_classify = 0
    total = 0
    for file in files:
        total += 1
        data = parse_image(testdir + file)
        print "testing:", file
        num = int(file[0])
        classify_failed = True
        for i in range(10):
            pvalue = predict(G_WEIGHT[i], data)
            if pvalue > 0:
                classify_failed = False
                print i, "prdict:", 1
                if i == num:
                    right += 1
                else:
                    wrong += 1
            else:
                print i, "prdict:", -1
        if classify_failed:
            can_not_classify += 1
        
    print "right=", right
    print "wrong=", wrong
    print "can_not_classify=", can_not_classify
    print "total=", total
        
