import pandas as pd
import numpy as np
import time

class DataFrameTransformer():
    def __init__(self, func, source_columns=None):
        self.name = 'DataFrameTransformer'
        self.source_columns = source_columns
        self.func = func

    def fit(self, X, y=None, **fit_params):
        start = time.time()
        #
        end = time.time()
        print(f"{self.name} fit successfully in {end-start:.2f} s")
        return self

    def transform(self, X, **transform_params):
        data = X.copy()
        if self.source_columns != None:
            data = self.func(data, self.source_columns)
        else:
            data = self.func(data)
        return data

    def execute(self, X):
        self.fit(X)
        return self.transform(X)