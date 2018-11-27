from sklearn.preprocessing import Normalizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
from joblib import dump,load
import numpy as np
import pandas as pd
from sklearn.utils import shuffle

class pedAccidents:
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
        
if __name__ == '__main__':
    collisions_attr_df = pd.read_csv('data/surroundings.csv', engine='python',sep = ',')
    collisions_attr_df1 = pd.read_csv('data/collisions_attr_temp.csv', engine='python',sep = ',')
    temp_df = pd.concat([collisions_attr_df[['eat-drink', 'restaurant', 'snacks-fast-food', 'bar-pub', 'coffee-tea', 'coffee', 'tea', 'going-out', 'dance-night-club', 'cinema', 'theatre-music-culture', 'casino', 'sights-museums', 'landmark-attraction', 'museum', 'transport', 'airport', 'railway-station', 'public-transport', 'ferry-terminal', 'taxi-stand', 'accommodation', 'hotel', 'motel', 'hostel', 'camping', 'shopping', 'kiosk-convenience-store', 'wine-and-liquor', 'mall', 'department-store', 'food-drink', 'bookshop', 'pharmacy', 'electronics-shop', 'hardware-house-garden-shop', 'clothing-accessories-shop', 'sport-outdoor-shop', 'shop', 'business-services', 'atm-bank-exchange', 'police-emergency', 'ambulance-services', 'fire-department', 'police-station', 'post-office', 'tourist-information', 'petrol-station', 'ev-charging-station', 'car-rental', 'car-dealer-repair', 'travel-agency', 'communication-media', 'business-industry', 'service', 'facilities', 'hospital-health-care-facility', 'hospital', 'government-community-facility', 'education-facility', 'library', 'fair-convention-facility', 'parking-facility', 'toilet-rest-area', 'sports-facility-venue', 'facility', 'religious-place', 'leisure-outdoor', 'recreation', 'amusement-holiday-park', 'zoo', 'administrative-areas-buildings', 'administrative-region', 'city-town-village', 'outdoor-area-complex', 'building', 'street-square', 'intersection', 'postal-area', 'natural-geographical', 'body-of-water', 'mountain-hill', 'undersea-feature', 'forest-heath-vegetation', 'lots_of_places']],collisions_attr_df1[:50000][['PEDESTRIAN_ACCIDENT', 'BICYCLE_ACCIDENT', 'MOTORCYCLE_ACCIDENT', 'TRUCK_ACCIDENT', 'COUNT_PED_KILLED', 'COUNT_PED_KILLED.1', 'COUNT_BICYCLIST_KILLED', 'COUNT_MC_KILLED', 'COUNTY', 'CITY', 'NUMBER_KILLED', 'POINT_X', 'POINT_Y', 'weatherA', 'weatherB', 'weatherC', 'weatherD', 'weatherE', 'weatherF', 'weatherG', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE', 'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E', 'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B', 'road_surface_C', 'road_surface_D', 'collision_time']]],axis=1)
    temp_df = shuffle(temp_df).reset_index(drop = True)
    temp_df=temp_df[(np.isnan(temp_df.POINT_X) == False) & (np.isnan(temp_df.POINT_Y) == False)]
    df = temp_df[['eat-drink', 'restaurant', 'snacks-fast-food', 'bar-pub', 'coffee-tea', 'coffee', 'tea', 'going-out', 'dance-night-club', 'cinema', 'theatre-music-culture', 'casino', 'sights-museums', 'landmark-attraction', 'museum', 'transport', 'airport', 'railway-station', 'public-transport', 'ferry-terminal', 'taxi-stand', 'accommodation', 'hotel', 'motel', 'hostel', 'camping', 'shopping', 'kiosk-convenience-store', 'wine-and-liquor', 'mall', 'department-store', 'food-drink', 'bookshop', 'pharmacy', 'electronics-shop', 'hardware-house-garden-shop', 'clothing-accessories-shop', 'sport-outdoor-shop', 'shop', 'business-services', 'atm-bank-exchange', 'police-emergency', 'ambulance-services', 'fire-department', 'police-station', 'post-office', 'tourist-information', 'petrol-station', 'ev-charging-station', 'car-rental', 'car-dealer-repair', 'travel-agency', 'communication-media', 'business-industry', 'service', 'facilities', 'hospital-health-care-facility', 'hospital', 'government-community-facility', 'education-facility', 'library', 'fair-convention-facility', 'parking-facility', 'toilet-rest-area', 'sports-facility-venue', 'facility', 'religious-place', 'leisure-outdoor', 'recreation', 'amusement-holiday-park', 'zoo', 'administrative-areas-buildings', 'administrative-region', 'city-town-village', 'outdoor-area-complex', 'building', 'street-square', 'intersection', 'postal-area', 'natural-geographical', 'body-of-water', 'mountain-hill', 'undersea-feature', 'forest-heath-vegetation', 'lots_of_places', 'weatherA', 'weatherB', 'weatherC', 'weatherD', 'weatherE', 'weatherF', 'weatherG', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'lightingA', 'lightingB', 'lightingC', 'lightingD', 'lightingE', 'road_cond_A', 'road_cond_B', 'road_cond_C', 'road_cond_D', 'road_cond_E', 'road_cond_F', 'road_cond_G', 'road_cond_H', 'road_surface_A', 'road_surface_B', 'road_surface_C', 'road_surface_D']]

    y_label = temp_df[['PEDESTRIAN_ACCIDENT']]
    ped_accidents = pedAccidents()
    ped_accidents.trainModel(df,y_label)
    ped_accidents.save("models/pedAccidents")