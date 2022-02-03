#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Wed Jan 26 07:24:05 2022@author: William Bennett"""import numpy as npfrom numba import int64, float64, jit, njit, deferred_typefrom numba.experimental import jitclass# from main import IC_func from mesh import mesh_classfrom functions import normPnfrom mutables import IC_func###############################################################################mesh_class_type = deferred_type()mesh_class_type.define(mesh_class.class_type.instance_type)IC_func_type = deferred_type()IC_func_type.define(IC_func.class_type.instance_type)data = [('N_ang', int64),         ('N_space', int64),        ('M', int64),        ('tfinal', float64),        ('sigma_t', float64[:]),        ('sigma_s', float64[:]),        ('IC', float64[:,:,:]),        ('mus', float64[:]),        ('ws', float64[:]),        ('xs_quad', float64[:]),        ('ws_quad', float64[:]),        ('x0', float64),        ("source_type", int64[:]),        ("uncollided", int64),        ("moving", int64),        ("move_type", int64[:]),        ("time", int64),        ("plotting", int64),        ("RMS", int64)        ]###############################################################################    @jitclass(data)class build(object):    def __init__(self, N_ang, N_space, M, tfinal, x0, mus, ws, xs_quad, ws_quad, sigma_t, sigma_s, source_type,                 uncollided, moving, move_type, time, plotting, RMS):        self.N_ang = N_ang        self.N_space = N_space        self.M = M        self.tfinal = tfinal        self.sigma_t = sigma_t        self.sigma_s = sigma_s        self.IC = np.zeros((N_ang, N_space, M+1))        self.mus = mus        self.ws = ws/np.sum(ws)        self.xs_quad = xs_quad        self.ws_quad = ws_quad        self.x0 = x0        self.source_type = source_type        self.uncollided = uncollided         self.moving = moving        self.move_type = move_type        self.time = time        self.plotting = plotting        self.RMS = RMS            def integrate_quad(self, a, b, ang, space, j, ic):        self.IC[ang,space,j] = (b-a)/2 * np.sum(self.ws_quad * ic.function((b-a)/2*self.xs_quad + (a+b)/2) * normPn(j, self.xs_quad, -1.0, 1.0))                    def make_IC(self):        edges = mesh_class(self.N_space, self.x0, self.tfinal, self.moving, self.move_type)                edges_init = edges.edges        ic = IC_func(self.source_type, self.uncollided)        for ang in range(self.N_ang):            for space in range(self.N_space):                for j in range(self.M):                    self.integrate_quad(edges_init[space], edges_init[space+1], ang, space, j, ic)                                            