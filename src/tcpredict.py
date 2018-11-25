from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
from joblib import dump,load
import numpy as np
import pandas as pd
from sklearn.utils import shuffle

class tcAccidents:
    normalizer = Normalizer(norm ='l2')
    dimRed = SelectKBest(chi2, k=10)
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
		
if __name__ == '__main__':
	collisions_attr_df = pd.read_csv('data/collisions_attr_temp.csv', engine='python',sep = ',')
	temp_df = collisions_attr_df[collisions_attr_df.TRUCK_ACCIDENT == 'N'][:813].append(collisions_attr_df[collisions_attr_df.TRUCK_ACCIDENT == 'Y'])
	temp_df = shuffle(temp_df).reset_index(drop = True)
	temp_df=temp_df[(np.isnan(temp_df.POINT_X) == False) & (np.isnan(temp_df.POINT_Y) == False)]
	df = temp_df[['weatherA', 'weatherB', 'weatherC', 'weatherD',\
				  'weatherE', 'weatherF', 'weatherG', 'monday',\
				  'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',\
				  'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE',\
				  'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E',\
				  'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B',\
				  'road_surface_C', 'road_surface_D', 'collision_time','POINT_X','POINT_Y']]

	df.POINT_X=df.POINT_X*(-1)
	y_label = temp_df[['TRUCK_ACCIDENT']]
	tc_accidents = tcAccidents()
	tc_accidents.trainModel(df,y_label)
	tc_accidents.save("models/tcAccidents")