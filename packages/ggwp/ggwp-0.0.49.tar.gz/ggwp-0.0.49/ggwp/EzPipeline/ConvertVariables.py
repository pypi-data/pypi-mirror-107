import pandas as pd
import numpy as np
import time


class ConvertVariables():
    def __init__(self, conversion_dict):
        """
        name: function name
        conversion_dict: dtypes and columns
        """
        self.name = 'ConvertVariables'
        self.conversion_dict = conversion_dict

    def convert_dtypes(self, X):
        data = X.copy()
        for d_type, cols in self.conversion_dict.items():
            data[cols] = data[cols].astype(d_type)

        return data

    def fit(self, X, y=None, **fit_params):
        start = time.time()
        #
        end = time.time()
        print(f"{self.name} fit successfully in {end-start:.2f} s")
        return self
        
    def transform(self, X, **transform_params):       
        return self.convert_dtypes(X)

    def execute(self, X):
        self.fit(X)
        return self.transform(X)