import pandas as pd
import numpy as np
import time
import functools
import operator

class OneHotTransformer():
    def __init__(self, target_columns):
        self.name = 'OneHotTransformer'
        self.target_columns = target_columns
        self.unique_values = []

    def get_unique(self, X):
        unique_values = []
        for column in self.target_columns:
            unique = list(X[column].unique())
            unique.sort()
            unique_values.append(unique)
        return unique_values

    def get_onehot(self, X):
        for enum, column in enumerate(self.target_columns):
            unique_values = self.unique_values[enum]
            for unique_value in unique_values:
                X[f"{column}_{unique_value}"] = np.where(X[column]==unique_value, 1, 0)
        return X.drop(self.target_columns, axis=1)

    def fit(self, X, y=None, **fit_params):
        start = time.time()
        self.unique_values = self.get_unique(X)
        end = time.time()
        print(f"{self.name} fit successfully in {end-start:.2f} s")
        return self

    def transform(self, X, **transform_params):
        data = X.copy()
        unique_values = self.get_unique(X)
        if unique_values !=  self.unique_values:
            raise ValueError("New values did not match. Please re-check your data again")
        else:
            return self.get_onehot(data)


    def execute(self, X):
        self.fit(X)
        return self.transform(X)