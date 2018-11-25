
# coding: utf-8

# In[306]:


import numpy as np
import pandas as pd
import scipy.sparse as sp
from numpy.linalg import norm





import math as m
def formatTime(time):
    minutes = m.floor((time/100))*60 + time%100
    return minutes


# In[380]:


#create column for each condition
def getConditions(weather,day,lighting,roadcond,roadsurface,time):
    t=formatTime(time)
    w = {}
    aw = {}
    for i in 'ABCDEFGH':
        w[i] = 0
        aw[i] = 0
   
    d = {}
    for i in range(1,7):
        d[i] = 0
    
    l = {}
    for i in 'ABCDEF':
        l[i] = 0
        
    rc = {}
    arc = {}
    for i in 'ABCDEFGHI':
        rc[i] = 0
        arc[i] = 0
        
    rs= {}
    for i in 'ABCDE':
        rs[i] = 0
        
    w[weather] =1
    d[day] = 1
    l[lighting] =1
    rc[roadcond] =1
    rs[roadsurface] =1
    
    return w,d,l,rc,rs,t


# In[381]:


def processInput(weather,day,road_cond,road_surface,lighting,collisiontime,x,y):
    w,d,l,rc,rs,t = getConditions(weather, day,lighting,road_cond,road_surface,collisiontime)
    collisions_attr_df = pd.DataFrame({'weatherA':w['A'],'weatherB':w['B'],'weatherC':w['C'],'weatherD':w['D'],                                   'weatherE':w['E'],'weatherF':w['F'],'weatherG':w['G'],'monday': d[1],                                   'tuesday': d[2], 'wednesday': d[3], 'thursday': d[4],                                   'friday': d[5], 'saturday': d[6],'lightingA':l['A'], 'lightingB':l['B'],                                       'lightingC':l['C'], 'lightingD':l['D'], 'lightingE':l['E'],                                   'road_cond_A':rc['A'], 'road_cond_B':rc['B'],'road_cond_C':rc['C'],                                   'road_cond_D':rc['D'],'road_cond_E':rc['E'], 'road_cond_F':rc['F'],                                   'road_cond_G':rc['G'], 'road_cond_H':rc['H'],'road_surface_A':rs['A'],                                   'road_surface_B':rs['B'], 'road_surface_C':rs['C'],'road_surface_D':rs['D'],                                   'collision_time':t,'point_x':x,'point_y':y},index=[0])
    return collisions_attr_df


