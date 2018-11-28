import warnings
import pandas as pd
import statsmodels.api as sm
from flask import jsonify
warnings.filterwarnings("ignore")


class TimeSeriesPrediction:
    dateColumn = 'COLLISION_DATE'
    injuredColumn = 'NUMBER_INJURED'
    killedColumn = 'NUMBER_KILLED'
    pedestrian_injured = 'COUNT_PED_INJURED'
    bicyclist_injured = 'COUNT_BICYCLIST_INJURED'
    dateFormat = '%Y-%m-%d'
    fileLocation = 'data/collisions.csv'

    def __init__(self):
        date_column = TimeSeriesPrediction.dateColumn
        self.df = pd.read_csv(TimeSeriesPrediction.fileLocation, engine='python', sep=',')
        self.df[date_column] = pd.to_datetime(self.df[date_column], format=TimeSeriesPrediction.dateFormat)

    def predict_injured(self, county, years):
        return self.predict_for_column(TimeSeriesPrediction.injuredColumn, county, years)

    def predict_killed(self, county, years):
        return self.predict_for_column(TimeSeriesPrediction.killedColumn, county, years)

    def predict_pedestrian_injured(self, county, years):
        return self.predict_for_column(TimeSeriesPrediction.pedestrian_injured, county, years)

    def predict_bicyclist_injured(self, county, years):
        return self.predict_for_column(TimeSeriesPrediction.bicyclist_injured, county, years)

    def predict_for_column(self, prediction_column, county, years):
        periods = 12 * years
        date_column = TimeSeriesPrediction.dateColumn
        df = self.df.copy()

        # if county is null all data will be processed
        if county:
            match = df['COUNTY'] == county
            df = df[match]

        if df.empty:
            return jsonify({
                "status": 500,
                "error": "No data found for the county",
                "x_observed": [],
                "y_observed": [],
                "x_prediction": [],
                "y_prediction": []
            })

        df = df.groupby(date_column)[prediction_column].sum().reset_index()
        df = df.set_index(date_column)

        observed = df[prediction_column].resample('MS').sum()

        model = sm.tsa.statespace.SARIMAX(observed,
                                        order=(1, 1, 1),
                                        seasonal_order=(1, 1, 0, 12),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        results = model.fit()

        prediction = results.get_forecast(steps=periods)

        df = pd.DataFrame({
            'date': prediction.predicted_mean.index,
            prediction_column: prediction.predicted_mean.values})

        df['date'] = pd.to_datetime(df['date'], format=TimeSeriesPrediction.dateFormat)

        aggregated_prediction = df.groupby(df['date'].dt.year).agg({prediction_column: 'sum'})

        x_prediction = []
        y_prediction = []
        for row in aggregated_prediction.iterrows():
            x_prediction.append(row[0])
            y_prediction.append(int(row[1].values[0]))

        df = pd.DataFrame({
            'date': observed.index,
            prediction_column: observed.values})

        df['date'] = pd.to_datetime(df['date'], format=TimeSeriesPrediction.dateFormat)

        aggregated_observed = df.groupby(df['date'].dt.year).agg({prediction_column: 'sum'})

        x_observed = []
        y_observed = []
        for row in aggregated_observed.iterrows():
            x_observed.append(row[0])
            y_observed.append(int(row[1].values[0]))

        return jsonify({
            "status": 200,
            "x_observed": x_observed,
            "y_observed": y_observed,
            "x_prediction": x_prediction,
            "y_prediction": y_prediction
        })
