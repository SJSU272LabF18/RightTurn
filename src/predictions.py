
# coding: utf-8

# In[306]:


import numpy as np
import pandas as pd
import scipy.sparse as sp
from numpy.linalg import norm


# In[307]:


collisions_attr_df = pd.read_csv('data/collisions_attr_temp.csv', engine='python',sep = ',')


# In[369]:


from sklearn.utils import shuffle
temp_df = collisions_attr_df
temp_df = shuffle(temp_df).reset_index(drop = True)
temp_df=temp_df[(np.isnan(temp_df.POINT_X) == False) & (np.isnan(temp_df.POINT_Y) == False)]
df = temp_df[['weatherA', 'weatherB', 'weatherC', 'weatherD',              'weatherE', 'weatherF', 'weatherG', 'monday',              'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',              'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE',              'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E',              'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B',              'road_surface_C', 'road_surface_D', 'collision_time','POINT_X','POINT_Y']]

df.POINT_X=df.POINT_X*(-1)


# In[374]:


y_label = temp_df[['PEDESTRIAN_ACCIDENT']]


# In[375]:


df_train = df
from sklearn.preprocessing import Normalizer
transformer = Normalizer(norm ='l2').fit(df_train)
transformer.transform(df_train)
def normalize(test):
    transformer = Normalizer(norm ='l2').fit(test)
    transformer.transform(test)
    return test


# In[376]:


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
chisq = SelectKBest(chi2, k=10)
train = chisq.fit_transform(df_train, y_label)
def dimRed(test):
    test=chisq.transform(test)
    return test


# In[384]:


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(C=0.1,penalty = 'l2',random_state=0, solver='liblinear',multi_class='ovr').fit(train,y_label)
def predictLogReg(test):
    pred = clf.predict(test)
    return pred.tolist()


# In[385]:


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=5, max_depth=10,random_state=0)
clf.fit(train, y_label)
def predictRandomForest(test):
    test = normalize(test)
    test = dimRed(test)
    pred = clf.predict(test)
    return  pred.tolist()


# In[379]:


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


# In[ ]:


def predictPI(weather,day,road_cond,road_surface,lighting,collisiontime,x,y):
    test_df = processInput(weather,day,road_cond,road_surface,lighting,collisiontime,x,y)
    return predictRandomForest(test_df)

