import pandas as pd
import numpy as np
import time

class ColumnAssignment():
    def __init__(self, target_column, func, source_columns):
        self.name = 'ColumnAssignment'
        self.target_column = target_column
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
        data[self.target_column] = self.func(data, self.source_columns)
        return data

    def execute(self, X):
        self.fit(X)
        return self.transform(X)