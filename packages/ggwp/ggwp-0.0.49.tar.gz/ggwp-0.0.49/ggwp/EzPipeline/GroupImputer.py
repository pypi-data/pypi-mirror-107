import pandas as pd
import numpy as np
import time


class GroupImputer():
    def __init__(self, grp_cols, target_col, aggfunc):
        """
        name: function name
        grp_cols: masking criteria
        target_col: column to be imputed
        aggfunc: aggregation
        lookup: look-up table
        """
        self.name = 'GroupImputer'
        self.grp_cols = grp_cols
        self.target_col = target_col
        self.aggfunc = aggfunc
        self.lookup = pd.DataFrame()

    def multiple_grp(self,X):

        data = X.copy()
        res = data.groupby(self.grp_cols).agg({self.target_col:self.aggfunc})
        self.lookup = res.reset_index()
        return self.lookup

    def multiple_impute(self, X):

        data = X.copy()
        for idx in range(self.lookup.shape[0]):
            mask = True
            value = self.target_col
            for column in self.grp_cols:
                mask = mask & (data.loc[:, column]==self.lookup.loc[idx, column])
            mask = mask & (data[value].isna())
            data.loc[mask, value] = self.lookup.loc[idx, value]
        return data

    def fit(self, X, y=None, **fit_params):
        start = time.time()
        self.multiple_grp(X)
        end = time.time()
        print(f"{self.name} fit successfully in {end-start:.2f} s")
        return self
        
    def transform(self, X, **transform_params):       
        return self.multiple_impute(X)

    def execute(self, X):
        self.fit(X)
        return self.transform(X)