#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 18:18:04 2017

@author: sdwij3
"""

def index_bus():
 #bus : Bus num
 #bus_type : 
 #Pd : demand
 #basekV
    bus      = 0
    bus_type = 1
    Pd       = 2
    basekV   = 3
    return (bus,bus_type,Pd,basekV)


def index_gen():
#gennum : Generator number for 
#conbus : Connected bus number
#tind   : technology index (fuel type)
#   1=wind offshore, 2 = wind onshore 3 = solar(pv), 4 = coal , 5 = gas   6=diesel
#Pmax :  Maximum capacity (Rated Capacity) MW
#Pmin :  Minim capacity  MW
# ints :initial state 0-not operating 1-fully operating
# cony : number of years to complete constructions from current year
#            0 indicates its currently in operation
# eofy : number of years for end of life from current year
    gennum = 0 ;
    conbus = 1 ;
    tind   = 2 ;   
    Pmax   = 3 ;
    Pmin   = 4 ;
    ints   = 5 ;
    cony   = 6 ;            
    eofy   = 7 ;
    return (gennum,conbus,tind,Pmax,Pmin,ints,cony,eofy)


def index_line():
 #lnum : line number
 #fbus  : starting bus
 #tbus  : ending bus
 #y     : reactance p.u
 #ratep : maximum flow positive direction
 #raten : maximum flow negative direction
 #ltype : type of transmission line 1:AC
 #dist     : Distance of the new line in km
     lnum   = 0;
     fbus   = 1;
     tbus   = 2;
     X      = 3;
     ratep  = 4;
     raten  = 5;
     ltype  = 6;
     dist   = 7;
     return (lnum,fbus,tbus,X,ratep,raten,ltype,dist)
 

def index_gencost():
#cost_type : peicewise linear or polynomial
#startup   : startup cost
#shutdown  : shutdown cost
#ncoeff    : number of cost coefficients;
#C2        : c(n-1);
#C1        : .....;
#C0        : c0;
    cost_type = 0;
    startup   = 1;
    shutdown  = 2;
    ncoeff    = 3;
    C2        = 4;
    C1        = 5;
    C0        = 6;
    return (cost_type,startup,shutdown,ncoeff,C2,C1,C0)