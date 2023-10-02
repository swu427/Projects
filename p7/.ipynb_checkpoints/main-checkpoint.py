# project: p7
# submitter: swu427
# partner: none
# hours: 10

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split, cross_val_score



class UserPredictor:
    def __init__(self):
        
        self.xcols = ["age", "past_purchase_amt", "badge", "seconds"]
        self.numerical_values = ["age", "past_purchase_amt", "seconds"]
    
    def fit(self, train_users, train_logs, train_y):
        train_logs = train_logs.groupby("user_id")["seconds"].sum()
        df = pd.merge(train_users, train_logs, how = "left", on = "user_id").fillna(0)
        
        custom_transformer = make_column_transformer(
            (PolynomialFeatures(degree=2), self.numerical_values))
        
        self.model = Pipeline([
            ("custom", custom_transformer),
            ("st", StandardScaler()),
            ("lr", LogisticRegression(fit_intercept = False)),
        ])

        self.model.fit(df[self.xcols], train_y["y"])

    def predict(self, train_users, train_logs):
        train_logs = train_logs.groupby("user_id")["seconds"].sum()
        df = pd.merge(train_users, train_logs, how = "left", on = "user_id").fillna(0)
        return self.model.predict(df[self.xcols])

