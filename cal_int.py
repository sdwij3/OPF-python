#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:41:27 2017

@author: sdwij3
"""

import numpy as np
import math
#from random import randint

def formatcase(ppc):

    #Default values
    #a = 6; #lower bound for technology interval
    #b = 8; #upper bound for technology interval
    
    data = {}

    #Base value in MVA
    data['baseMVA'] = ppc['baseMVA']

    #Bus data
    N = len(ppc['bus'])
    data['bus'] = np.empty([N,4])
    data['bus'][:,0] = ppc['bus'][:,0]
    data['bus'][:,1] = ppc['bus'][:,1]
    data['bus'][:,2] = ppc['bus'][:,2]
    data['bus'][:,3] = ppc['bus'][:,9]

    #Existing generator data
    G = len(ppc['gen'])
    data['gen_ex'] = np.empty([G,8])
    data['gen_ex'][:,0] = range(1,G+1)
    data['gen_ex'][:,1] = ppc['gen'][:,0]
    data['gen_ex'][:,2] = range(1,G+1)
    data['gen_ex'][:,3] = ppc['gen'][:,8]
    data['gen_ex'][:,4] = ppc['gen'][:,9]
    data['gen_ex'][:,5] = np.ones(G)
    data['gen_ex'][:,6] = np.zeros(G)
    data['gen_ex'][:,7] = np.full((G),20)
    
    #Existing branch data 
    L = len(ppc['branch'])
    data['line_ex'] = np.empty([L,6])
    data['line_ex'][:,0] = range(1,L+1);
    data['line_ex'][:,1] =  ppc['branch'][:,0]
    data['line_ex'][:,2] =  ppc['branch'][:,1]
    data['line_ex'][:,3] =  ppc['branch'][:,3]
    data['line_ex'][:,4] =  ppc['branch'][:,5]
    data['line_ex'][:,5] = -ppc['branch'][:,5]
        
    #Gencost
    data['gencost_ex'] = ppc['gencost']
    return data
                 

def getgenmat(num_nodes,num_gens,con_bus):
    genmat = np.zeros([num_nodes,num_gens])
    for n in range(num_nodes):
        for g in range(num_gens):
            if con_bus[g] == (n+1):
                genmat[n,g] = 1;
    return genmat


def getlinemat(num_nodes,num_lines,from_bus,to_bus):
    linemat = np.zeros([num_nodes,num_lines]);
    for  n in range(num_nodes):
        for l in range(num_lines):
            if from_bus[l] == (n+1):
                linemat[n,l]= -1;
            if to_bus[l] == (n+1):
                linemat[n,l] = 1;
    return linemat

def getsucepcoeff(baseMVA,basekV,X):
    #Calculating susceptance in mho
    V_phase = max(basekV)/math.sqrt(3);
    X_base = math.pow(V_phase,2)/math.pow(baseMVA,2);
    b_coeff = X_base*np.array(X); 
    #because matpower gives reactance x, so susceptance = 1/x
    #but f/b = fx so coeffient is xbase*x
    return  b_coeff