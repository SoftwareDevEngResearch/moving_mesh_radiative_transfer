#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Wed Jan 26 07:24:05 2022@author: William Bennett"""import numpy as npfrom numba import int64, float64from numba.experimental import jitclass###############################################################################data = [('N_ang', int64),         ('N_space', int64),        ('M', int64),        ('tfinal', float64),        ('mus', float64[:]),        ('ws', float64[:]),        ('x0', float64),        ("moving", int64),        ("move_type", int64[:]),        ("edges", float64[:]),        ("Dedges", float64[:])        ]###############################################################################    @jitclass(data)class mesh_class(object):    def __init__(self, N_space, x0, tfinal, moving, move_type):        self.tfinal = tfinal        self.N_space = N_space        self.x0 = x0        self.moving = moving        self.move_type = move_type        self.edges = np.zeros(N_space+1)        self.Dedges = np.zeros(N_space+1)        self.initialize_mesh()                    def move(self, t):        if self.moving == True and self.move_type[0] == 1:            self.Dedges = self.edges/self.edges[-1]            self.edges += self.Dedges*np.abs(self.edges)*t                def initialize_mesh(self):        if self.moving != "static":            self.edges = np.linspace(-self.x0, self.x0, self.N_space+1)        else:            self.edges = np.linspace(-self.tfinal, self.tfinal, self.N_space+1)        