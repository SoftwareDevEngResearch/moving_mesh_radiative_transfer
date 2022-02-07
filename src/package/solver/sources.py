#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 14:38:34 2022

@author: bennett
"""
import numpy as np
from build_problem import build
import math
from functions import normPn

from numba import float64, int64, deferred_type
from numba.experimental import jitclass
###############################################################################
build_type = deferred_type()
build_type.define(build.class_type.instance_type)

data = [("S", float64[:]),
        ("source_type", int64[:]),
        ("uncollided", int64),
        ("M", int64),
        ("x0", float64),
        ("t", float64),
        ("xL", float64),
        ("xR", float64),
        ("argument", float64[:]),
        ("source_vector", float64[:]),
        ("temp", float64[:]),
        ("abxx", float64),
        ("xx", float64),
        ("ix", int64),
        ("xs_quad", float64[:]),
        ("ws_quad", float64[:]),
        ("mag", float64)
        ]
###############################################################################
@jitclass(data)
class source_class(object):
    def __init__(self, build):
        self.S = np.zeros(build.M+1).transpose()
        self.source_type = build.source_type
        self.uncollided = build.uncollided
        self.x0 = build.x0
        self.M = build.M
        self.xs_quad = build.xs_quad
        self.ws_quad = build.ws_quad
        
    def integrate_quad(self, t, a, b, j, source_vector):
        argument = (b-a)/2*self.xs_quad + (a+b)/2
        self.S[j] = (b-a)/2 * np.sum(self.ws_quad * source_vector * normPn(j, argument, a, b))
        
    def square_IC_uncollidided_source(self, xs, t):
        temp = xs*0
        for ix in range(xs.size):
            xx = xs[ix]
            abxx = abs(xx)
            if (abxx <= t + self.x0) and (abxx <= t - self.x0):
                mag = math.exp(-t)/(4*t*t*self.x0 + 1e-12)
                temp[ix] = mag
            elif (xx < t + self.x0) and (xx > -t - self.x0):
                if (self.x0 - xx >= t) and (self.x0 + xx <= t):
                    temp[ix] = math.exp(-t)*(t + xx + self.x0)/(4.0*t*t*self.x0 + 1e-12)
                elif (self.x0 - xx <= t) and (self.x0 + xx >= t):
                    temp[ix] = math.exp(-t)*(t - xx + self.x0)/(4.0*t*t*self.x0 + 1e-12)
                else:
                    temp[ix] = 0.0
            else: 
                temp[ix] = 0.0
        return temp/2.0
    

        return temp
    def plane_IC_uncollided_source_integrated(self, t, xL, xR):
        self.S[0] = (math.exp(-t)/(2*t+self.x0)*math.sqrt(xR-xL))/2
        
    def make_source(self, t, xL, xR):
        if self.uncollided == True:
            if self.source_type[0] == 1:
                self.plane_IC_uncollided_source_integrated(t, xL, xR)
            elif self.source_type[1] == 1:
                for j in range(self.M+1):
                    argument = (xL-xR)/2*self.xs_quad + (xL+xR)/2
                    source_vector= self.square_IC_uncollidided_source(argument, t)
                    self.integrate_quad(t, xL, xR, j, source_vector)
                
                
            