from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
from joblib import dump,load
import numpy as np
import pandas as pd
from sklearn.utils import shuffle

class bcAccidents:
    normalizer = Normalizer(norm ='l2')
    dimRed = SelectKBest(chi2, k=30)
    model = clf = RandomForestClassifier(n_estimators=5, max_depth=10,random_state=0)
    
    def fitNormalizer(self,train):
        self.normalizer.fit(train)
    
    def normalize(self,test):
        return self.normalizer.transform(test)
        
    def fitReducer(self,train,y):
        self.dimRed.fit(train,y)
    
    def reduce(self,test):
        return self.dimRed.transform(test)
    
    def trainModel(self,train,y):
        self.fitNormalizer(train)
        train = self.normalize(train)
        self.fitReducer(train,y)
        train = self.reduce(train)
        self.model.fit(train, y)
    
    def predict(self,test):
        test1 = self.normalize(test)
        test1 = self.reduce(test1)
        return self.model.predict(test1).tolist()
    
    def save(self,f_name):
        dump(self.normalizer, f_name+'_normalizer.joblib')
        dump(self.dimRed,f_name+'_reducer.joblib')
        dump(self.model,f_name+'_model.joblib')
        
    def load_model(self,f_name):
        self.normalizer = load(f_name+'_normalizer.joblib')
        self.dimRed = load(f_name+'_reducer.joblib')
        self.model = load(f_name+'_model.joblib')
    
    