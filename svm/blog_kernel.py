#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成展示核技巧的图片
# generate the picture for demonstrating the kernel method.

import sys
import random
import matplotlib.pyplot as plt
import pylab
import numpy as np
import math

if __name__ == "__main__":
    samples = []

    data_fn = "svm.kernel"

    fn = open(data_fn, "w")
    for i in range(0, 50):
        x1 = random.randint(-30, 30)
        x2 = random.randint(-30, 30)
        label = x1*x1 + x2*x2 - 23*23 
        if label < 50 and label > -30:
            i -= 1
            continue
        if math.fabs(x1) > 28 or math.fabs(x2) > 28:
            i -= 1
            continue
        if label > 0:
                label = 1
        else:
                label = -1
        print x1, x2, label
        fn.write("%d\t%d\t%d\n" %(x1, x2, label))
        samples.append((x1, x2, label))
    
    fn.close()    

    fig = plt.figure()
    ax = fig.add_subplot(1,2,1)
    plt.title("Data")
    ftrain = open(data_fn, "r")
    for line in ftrain:
        line = line[:-1]
        sam = line.split("\t")
        if int(sam[2]) > 0:
            ax.plot(sam[0],sam[1], 'or')
        else:
            ax.plot(sam[0],sam[1], 'og')
    ftrain.close()

    cir = pylab.Circle((0,0), radius=23,  fc='none')
    pylab.gca().add_patch(cir)
    ax.spines['left'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    pylab.text(-2, -35, "${x_1}$", {'color':'b','fontsize' : 20})
    pylab.text(-37, 0, "${x_2}$", {'color':'b','fontsize' : 20})
    ax.yaxis.set_ticks_position('left')

    ax = fig.add_subplot(1,2,2)
    ftrain = open(data_fn, "r")
    for line in ftrain:
        line = line[:-1]
        sam = line.split("\t")
        x1 = int(sam[0])
        x2 = int(sam[1])
        if int(sam[2]) > 0:
            ax.plot(x1*x1,x2*x2, 'or')
        else:
            ax.plot(x1*x1,x2*x2, 'og')
    ftrain.close()
    p1=[0,23*23]
    p2 = [23*23,0]
    pylab.gca().plot(p1,p2,'b')
    pylab.gca().set_xlabel("${x_1^2}$",{'color':'b','fontsize' : 20})
    pylab.text(-100, 500, "${x_2^2}$",{'color':'b','fontsize' : 20})
    pylab.gca().set_xlim(0,1000)
    pylab.gca().set_ylim(0,1000)
    plt.title("After $x_i^2$")
    plt.show()


