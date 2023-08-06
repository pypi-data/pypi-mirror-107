import pandas as pd
import numpy as np
from datetime import datetime
import time

from ggwp.EzUtils.EzUtils import EzUtils

class Check(EzUtils):
    def __init__(self):
        super().__init__()
        self.prep_data='EzCheck'

    def get_null(self, x):
        res = x.isna().sum()
        return res

    def get_dtypes(self, x):
        res = x.dtypes
        return res

    def get_nunique(self, x):
        res = x.nunique()
        return res

    def get_outlier(self, data):
        columns = data.columns.values
        res = []
        for col in columns:
            if data[col].dtypes.name in ['int8','int16','int32','int64',
                                           'float16','float32','float64']:
                q1,q3 = data[col].quantile([.25,.75])
                IQR = (q3-q1)*1.5
                lower_bound = q1-IQR
                upper_bound = q3+IQR

                if (data[col] < lower_bound).sum() != 0 | (data[col] > upper_bound).sum() != 0:
                    res.append('yes')
                else:
                    res.append('no')
            else:
                res.append('undefined')
        return res

    def convert_dtypes(self, data,column):
        pass

    def check(self, data, n=4):
        check_df = pd.DataFrame()
        data = data
        n_row, n_col = data.shape
        pipeline = {'dtypes':self.get_dtypes,'missing':self.get_null,
                    'missing_ratio':self.get_null,
                    'nunique':self.get_nunique,
                    'n_ratio':self.get_nunique}
        for col, func in pipeline.items():
            if 'ratio' not in col:
                check_df[col] = func(data)
            else:
                check_df[col] = func(data)/n_row

        check_df['outlier'] = self.get_outlier(data)

        return check_df.sort_index().round(n)

    def get_num(self,x):
        arr = pd.Series([x.count(),min(x),x.quantile(.25),x.median(),x.mean(),
                         x.quantile(.75),max(x),max(x)-min(x),x.skew(),x.std()], 
                        index=['count','min','25%','median','mean','75','max','range','skew','std'])
        return arr

    def get_obj(self,x):
        arr = pd.Series([x.count(),x.value_counts().index[0],x.value_counts().values[0],
                         x.value_counts().index[-1],x.value_counts().values[-1]],
                        index=['count','top','t_freq','least','l_freq'])
        return arr

    def get_date(self,x):
        arr = pd.Series([x.count(),x.min(),x.max(), x.max()-x.min()],
                        index=['count','min','max','day'])
        return arr

    def get_pattern(self, data, column, method='count'):
        start = time.time()
        arr = data[column].astype(str).copy()
        # EN
        arr = arr.str.replace(r"[a-zA-Z]","w")
        # TH
        arr = arr.str.replace(r"[\u0E00-\u0E7F]",'t')
        # Digit
        arr = arr.str.replace(r"[\d]","d")
        end = time.time()
        print(f"successfully executed {end-start:.2f} (s)")
        if method == 'count':
            return arr.value_counts()
        else:
            return arr

    def summary(self, data, method):
        start = time.time()
        data = data.select_dtypes(method)
        columns = data.columns
        summary_df = pd.DataFrame()
        for col in columns:

            if method=='number':
                summary_df[col] = self.get_num(data[col])
                
            elif method=='object':
                summary_df[col] = self.get_obj(data[col])

            elif method=='datetime':
                summary_df[col] = self.get_date(data[col])
        print(f'EzCheck for {method} successfully executed {time.time()-start:.2f} ms')
        return summary_df.T.round(4)

    def sumNum(self, data, method='number'):
        return self.summary(data, method)

    def sumCat(self, data, method='object'):
        return self.summary(data, method)

    def sumDate(self, data, method='datetime'):
        return self.summary(data, method)