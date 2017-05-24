#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 18:44:35 2017

@author: sdwij3
"""
from gurobipy import *
from index import *
from cal_int import *
from case6ww import *
import numpy as np

# Imort casefile
Data = formatcase(case6ww())

#Import indices
(busnum,bus_type,Pd,basekV) = index_bus()
(gennum,conbus,tind,Pmax,Pmin,ints,cony,eofy) = index_gen()
(lnum,fbus,tbus,X,ratep,raten,ltype,dist)=index_line()
(cost_type,startup,shutdown,ncoeff,C2,C1,C0)=index_gencost()

# Define parameters
num_nodes = len(Data['bus'])
num_gens= len(Data['gen_ex'])
num_lines = len(Data['line_ex'])
nodes = range(num_nodes)
gens_ex= range(num_gens)
lines_ex = range(num_lines)

#Index matricesfor generators,lines and phase angles              
genmat_ex = getgenmat(num_nodes,num_gens,Data['gen_ex'][:,conbus])
linemat_ex = getlinemat(num_nodes,num_lines,Data['line_ex'][:,fbus],Data['line_ex'][:,tbus])
angmat_ex = linemat_ex.transpose()
#Susceptance co-efficent for power flows in lines
B_coeff = getsucepcoeff(Data['baseMVA'],Data['bus'][:,basekV],Data['line_ex'][:,X])

# Create the gurobi model
GRBm = Model('operation')

# Add Variables:
# Power generation
y = GRBm.addVars(gens_ex,
                 lb = Data['gen_ex'][:,Pmin],
                 ub = Data['gen_ex'][:,Pmax],
                 name="gen")
#Power flow
f = GRBm.addVars(lines_ex,
                 lb = Data['line_ex'][:,raten],
                 ub = Data['line_ex'][:,ratep],
                 name="line")
#Phase angle
a = GRBm.addVars(nodes,
                lb = np.full(num_nodes,-360),
                ub = np.full(num_nodes, 360),
                name='node')
GRBm.update()

# Set objective :
obj = (quicksum(Data['gencost_ex'][g,C2]*y[g]*y[g]      # Quadratic co-efficent c2*y*y
      + Data['gencost_ex'][g,C1]*y[g] for g in gens_ex) # Linear co-efficent c1*y
      + np.sum(Data['gencost_ex'][:,C0]))               #Fixed cost c0
GRBm.setObjective(obj, GRB.MINIMIZE)

# Add constraints:
#Nodal Balance Constraint
for n in nodes :
    GRBm.addConstr(quicksum(genmat_ex[n,g]*y[g] for g in gens_ex) #Total generation in node n
    + quicksum(linemat_ex[n,l]*f[l] for l in lines_ex)            #Net flow at node n
    == Data['bus'][n,Pd] ,"C1")                                   #Demand at node n

#DC power flow constraints
for l in lines_ex :
    GRBm.addConstr(B_coeff[l]*f[l]                  # Susceptance co-efficient for line l
    + quicksum(angmat_ex[l,n]*a[n] for n in nodes)  # Angle difference for line l
    == 0 ,"C2") 
    
#reference phase angle zero
GRBm.addConstr( a[0] == 0 ,"C3")  #reference node: node 1 set to zero

# Solve the model :    
GRBm.optimize()

# Obtain Results :
if GRB.OPTIMAL == 2:
    print('\nTOTAL COSTS: %g' % GRBm.objVal)
    #for v in GRBm.getVars():
        #print(v.varName, v.x)
