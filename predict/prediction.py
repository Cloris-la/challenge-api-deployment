
from catboost import CatBoostRegressor
import pandas as pd


def predict(dataInput):
    
    model = CatBoostRegressor()
    model.load_model('model/robocop_model.cbm')
    dataOutput = model.predict(dataInput)
    return float(dataOutput[0])



