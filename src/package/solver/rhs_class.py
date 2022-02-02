#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 11:25:35 2022

@author: bennett
"""
import numpy as np
from build_problem import build
###############################################################################

class rhs_class():
    def __init__(self, build):
        self.N_ang = build.N_ang 
        self.N_space = build.N_space
        self.M = build.M
        self.mus = build.mus
    def __call__(self,t, V, mesh, matrices, num_flux, source, flux):
        print(t)
        V_new = V.copy().reshape((self.N_ang, self.N_space, self.M+1))
        V_old = V_new.copy()
        
        mesh.move(t)
        
        for space in range(0, self.N_space):
            
            xR = mesh.edges[space+1]
            xL = mesh.edges[space]
            dxR = mesh.Dedges[space+1]
            dxL = mesh.Dedges[space]
            L = matrices(xL, xR, dxL, dxR, "L")
            G = matrices(xL, xR, dxL, dxR, "G")
            P = flux(V_old[:,space,:])
            S = source(t, xR, xL)
            for angle in range(self.N_ang):
                mul = self.mus[angle]
                LU =  num_flux(mesh, V_old[angle,:,:], space, mul)
                U = np.zeros(self.M+1).transpose()
                U[:] = V_old[angle,space,:]
                RHS = np.dot(G,U) + -LU + mul*np.dot(L,U) - U + P + S
                V_new[angle,space,:] = RHS.transpose()
        return V_new.reshape(self.N_ang*self.N_space*(self.M+1))
            
       