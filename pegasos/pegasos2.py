#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pegasos implemented in Python
# an elegant version of pegasos.py using numpy

import os
import sys
import math
import numpy as np

G_WEIGHT = np.zeros((10,32*32), dtype=float) 

def parse_image(path):
    img_map = np.zeros((32,32), dtype = float)
    line_no = 0
    fp = open(path, "r") 
    for line in fp:
        line = line[:-2]
        img_map[line_no]=[int(x) for x in line]
        line_no += 1
    return img_map.ravel()

def predict(model, data):
    return np.inner(model, data)

def train_one_model(data, label, sampleNum, modelNum):
    pvalue = predict(G_WEIGHT[modelNum], data)
    # the hinge loss
    if pvalue * label >= 1: return
    
    # update model
    lambd = 0.5
    new_weight = G_WEIGHT[modelNum] * ( 1 - 1.0/sampleNum) + (1.0 / (lambd * sampleNum))*label*data

    # projection
    norm2 = np.linalg.norm(new_weight)
    if norm2 > (1/math.sqrt(lambd)):
        G_WEIGHT[modelNum] = new_weight/(norm2 * math.sqrt(lambd)) 
    else:
        G_WEIGHT[modelNum] = new_weight

def train_one_sample(data, num, sampleNum):
    for modelNum in range(10):
        label = -1
        if num == modelNum:
            label = 1
        train_one_model(data, label, sampleNum, modelNum)

if __name__== "__main__":
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
        
