#!/usr/bin/env python
# -*- coding: utf-8 -*-

### ###
# handwriting numbers OCR based on svm.
# data from "Machine Learning in Action" chapter 02.
# 基于SVM的手写数字的识别程序
# 数据：采用了《Machine Learning in Action》第二章的数据
### ###

import sys
import os
import math

class model:
    def __init__(self):
        self.a = []
        self.b = 0.0

class GV:
    def __init__(self):
        self.samples = []        # 样本数据
        self.tests = []          # 测试数据
        self.models = []         # 训练的模型
        self.diff_dict = []      # 用于缓存预测知与真实y之差Ei
        self.cur_mno = 0         # 当前正使用或训练的模型
        self.cache_kernel = []   # 缓存kernel函数的计算结果
        self.use_linear = False  # 是否使用线性核函数
        self.RBF_dlt = 10        # 径向基函数的宽度

    def init_models(self):
        for i in range(0, 10):
            m = model()
            for j in range(len(self.samples)):
                m.a.append(0)
            self.models.append(m)

    def init_cache_kernel(self):
        i = 0
        for mi in self.samples: 
            print i
            self.cache_kernel.append([])
            j = 0
            for mj in self.samples:
                if i > j:
                    self.cache_kernel[i].append(self.cache_kernel[j][i])
                else:
                    self.cache_kernel[i].append(kernel(mi,mj))
                j += 1
            i += 1

class image:
    def __init__(self):
        self.data = []
        self.num = 0
        self.label = []
        self.fn = ""
       
    def printself(self):
        print "data"
        for line in self.data:
            print line
        print "num", self.num
        print "label", self.label[gv.cur_mno]
        print "fn", self.fn 

# global variables
gv = GV()

def parse_image(path):
    img_map = []
    fp = open(path, "r") 
    for line in fp:
        line = line[:-2]
        img_map.append(line)
    return img_map

# load samples and tests
def loaddata(dirpath, col):
    files = os.listdir(dirpath)
    for file in files:
        img = image()
        img.data = parse_image(dirpath + file)
        img.num = int(file[0])
        img.fn = file
        col.append(img)

def kernel(mj, mi):
    if gv.use_linear == True:
        return kernel_linear(mj,mi)
    else:
        return kernel_RBF(mj,mi)

######
# 高斯核函数
######
def kernel_RBF(mj, mi):
    if mj == mi:
        return math.exp(0)
    dlt = gv.RBF_dlt
    ret = 0.0
    for i in range(len(mj.data)):
        for j in range(len(mj.data[i])):
            ret += math.pow(int(mj.data[i][j]) - int(mi.data[i][j]), 2)
    ret = math.exp(-ret/(2*dlt*dlt))
    return ret

######
# 线性
######
def kernel_linear(mj, mi):
    ret = 0.0
    for i in range(len(mj.data)):
        for j in range(len(mj.data[i])):
            ret += int(mj.data[i][j]) * int(mi.data[i][j])
    return ret


# g(x)
def predict(m):
    pred = 0.0
    for j in range(len(gv.samples)):
        if gv.models[gv.cur_mno].a[j] != 0:
            pred += gv.models[gv.cur_mno].a[j] * gv.samples[j].label[gv.cur_mno] * kernel(gv.samples[j],m)
    pred += gv.models[gv.cur_mno].b 
    return pred

# the same as predict(m), only with different parmaters
def predict_train(i):
    pred = 0.0
    for j in range(len(gv.samples)):
        if gv.models[gv.cur_mno].a[j] != 0:
            pred += gv.models[gv.cur_mno].a[j] * gv.samples[j].label[gv.cur_mno] * gv.cache_kernel[j][i]
    pred += gv.models[gv.cur_mno].b 
    return pred

# 决策函数对xi的预测值和真实值之差
def predict_diff_real(i):
    diff = predict_train(i)
    diff -= gv.samples[i].label[gv.cur_mno]
    return diff

# 优化计算Ei
def predict_diff_real_optimized(idx, i, new_ai, j, new_aj, new_b):
    diff = (new_ai - gv.models[gv.cur_mno].a[i])* gv.samples[i].label[gv.cur_mno] * gv.cache_kernel[i][idx]
    diff += (new_aj - gv.models[gv.cur_mno].a[j])* gv.samples[j].label[gv.cur_mno] * gv.cache_kernel[j][idx]
    diff += new_b - gv.models[gv.cur_mno].b
    diff += gv.diff_dict[idx]
    return diff


def init_predict_diff_real_dict():
    gv.diff_dict = []
    for i in range(len(gv.samples)):
        gv.diff_dict.append(predict_diff_real(i))

def update_diff_dict(i, new_ai, j, new_bj, new_b):
    for idx in range(len(gv.samples)):
        # 原来的函数
        # gv.diff_dict[idx] = predict_diff_real(idx)
        # 有优化后的
        gv.diff_dict[idx] = predict_diff_real_optimized(idx, i, new_ai, j, new_bj, new_b)

def update_samples_label(num):
    for img in gv.samples:
        if img.num == num:
            img.label.append(1)
        else:
            img.label.append(-1)

######
#  svmocr train
#  基于算法SMO
#  T: tolerance 误差容忍度(精度)
#  times: 迭代次数
#  C: 惩罚系数
#  Mno: 模型序号0到9
#  step: aj移动的最小步长
######
def SVM_SMO_train(T, times, C, Mno, step):
    time = 0
    gv.cur_mno = Mno
    update_samples_label(Mno)
    init_predict_diff_real_dict()
    updated = True
    while time < times and updated:
        updated = False
        time += 1
        for i in range(len(gv.samples)):
            ai = gv.models[gv.cur_mno].a[i]
            Ei = gv.diff_dict[i]

            # agaist the KKT
            if (gv.samples[i].label[gv.cur_mno] * Ei < -T and ai < C) or (gv.samples[i].label[gv.cur_mno] * Ei > T and ai > 0):
                for j in range(len(gv.samples)):
                    if j == i: continue
                    kii = gv.cache_kernel[i][i]
                    kjj = gv.cache_kernel[j][j]
                    kji = kij = gv.cache_kernel[i][j] 
                    eta = kii + kjj - 2 * kij 
                    if eta <= 0: continue
                    new_aj = gv.models[gv.cur_mno].a[j] + gv.samples[j].label[gv.cur_mno] * (gv.diff_dict[i] - gv.diff_dict[j]) / eta # f 7.106
                    L = 0.0
                    H = 0.0
                    a1_old = gv.models[gv.cur_mno].a[i]
                    a2_old = gv.models[gv.cur_mno].a[j]
                    if gv.samples[i].label[gv.cur_mno] == gv.samples[j].label[gv.cur_mno]:
                        L = max(0, a2_old + a1_old - C)
                        H = min(C, a2_old + a1_old)
                    else:
                        L = max(0, a2_old - a1_old)
                        H = min(C, C + a2_old - a1_old)
                    if new_aj > H:
                        new_aj = H
                    if new_aj < L:
                        new_aj = L
                    if abs(a2_old - new_aj) < step:
                        print "j = %d, is not moving enough" % j
                        continue

                    new_ai = a1_old + gv.samples[i].label[gv.cur_mno] * gv.samples[j].label[gv.cur_mno] * (a2_old - new_aj) # f 7.109 
                    new_b1 = gv.models[gv.cur_mno].b - gv.diff_dict[i] - gv.samples[i].label[gv.cur_mno] * kii * (new_ai - a1_old) - gv.samples[j].label[gv.cur_mno] * kji * (new_aj - a2_old) # f7.115
                    new_b2 = gv.models[gv.cur_mno].b - gv.diff_dict[j] - gv.samples[i].label[gv.cur_mno]*kji*(new_ai - a1_old) - gv.samples[j].label[gv.cur_mno]*kjj*(new_aj-a2_old)    # f7.116
                    if new_ai > 0 and new_ai < C: new_b = new_b1
                    elif new_aj > 0 and new_aj < C: new_b = new_b2
                    else: new_b = (new_b1 + new_b2) / 2.0

                    update_diff_dict(i, new_ai, j, new_aj, new_b)
                    gv.models[gv.cur_mno].a[i] = new_ai
                    gv.models[gv.cur_mno].a[j] = new_aj
                    gv.models[gv.cur_mno].b = new_b
                    updated = True
                    print "iterate: %d, changepair: i: %d, j:%d" %(time, i, j)
                    #break

# 测试数据
def test():
    recog = 0
    recog_correct = 0
    for img in gv.tests: 
        print "test for", img.fn
        for mno in range(10):
            gv.cur_mno = mno
            if predict(img) > 0:
                print mno
                print img.fn
                recog += 1
                if mno == int(img.fn[0]):
                    recog_correct += 1
                break
    print "recog:", recog
    print "recog_correct:", recog_correct
    print "total:", len(gv.tests)

def save_models():
    for i in range(10):
        fn = open("models/" + str(i) + "_a.model", "w")
        for ai in gv.models[i].a:
            fn.write(str(ai))
            fn.write('\n')
        fn.close()
        fn = open("models/" + str(i) + "_b.model", "w")
        fn.write(str(gv.models[i].b))
        fn.close()

def load_models():
    for i in range(10):
        fn = open("models/" + str(i) + "_a.model", "r")
        j = 0
        for line in fn:
            gv.models[i].a[j] = float(line)
            j += 1
        fn.close()
        fn = open("models/" + str(i) + "_b.model", "r")
        gv.models[i].b = float(fn.readline())
        fn.close()

if __name__ == "__main__":
    training = True
    loaddata("trainingDigits/", gv.samples)
    loaddata("testDigits/", gv.tests)    
    print len(gv.samples)
    print len(gv.tests)

    if training == True:
        gv.init_cache_kernel()
    gv.init_models()

    print "init_models done"

    T = 0.0001
    C = 10
    step = 0.0001
    gv.RBF_dlt = 8
    if training == True:
        for i in range(10):
            print "traning model no:", i
            SVM_SMO_train(T, 100, C, i, step)
        save_models()
    else:
        load_models()
        for i in range(10):
            update_samples_label(i)
    test()
