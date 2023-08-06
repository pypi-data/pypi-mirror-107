import pandas as pd
import numpy as np
from datetime import datetime
import time

from ggwp.EzUtils.EzUtils import EzUtils

class RFMT(EzUtils):
    def __init__(self):
        super().__init__()
        self.data = None
        self.date_df = None
        self.snapshot = None
        self.customerId = 'customerId'
        self.orderId = 'orderId'
        self.orderDate = 'orderDate'
        self.salesPrice = 'salesPrice'

    @property
    def clear_cach(self):
        self.data = None
        self.date_df = None
        self.snapshot = None

    @property
    def echo(self):
        print('EzRFM')

    # def get_q1(self,x):
    #     return x.quantile(.25)

    # def get_q3(self,x):
    #     return x.quantile(.75)

    def get_range(self,x):
        return x.max()-x.min()

    def get_recency(self,x):
        return (self.snapshot-x.max()).days

    def get_tenure(self,x):
        return (self.snapshot-x.min()).days

    def prep_rfmt(self, data):

        data = data.groupby(self.customerId).agg({
            self.orderDate:[self.get_recency, self.get_tenure],
            self.orderId:'nunique',
            self.salesPrice:['sum','min',self.get_q1,'mean','median',
                             self.get_q3,'max','std',self.get_range,'skew']
        }).reset_index()

        names = ['Recency','Tenure','Frequency', 'Monetary',
                 'MonetaryMin','MonetaryQ1','MonetaryMean','MonetaryMedian',
                 'MonetaryQ3','MonetaryMax','MonetaryStd','MonetaryRange','MonetarySkew']
        data.columns = [self.customerId] + ['total' +  name for name in names]
        
        column_display = ['Recency','Frequency', 'Monetary', 'Tenure',
                 'MonetaryMin','MonetaryQ1','MonetaryMean','MonetaryMedian',
                 'MonetaryQ3','MonetaryMax','MonetaryStd','MonetaryRange','MonetarySkew']
        data = data[[self.customerId] + ['total' +  col for col in column_display]]

        return data.fillna(0).round(2)

    def prep_rfmt_date(self, data, column, method):
        data = data.groupby([self.customerId, column]).agg({
            self.orderId:'nunique',
            self.salesPrice:'sum'
        }).reset_index()

        data = data.groupby(self.customerId).agg({
            column:'nunique',
            self.orderId:['mean','median','std'],
            self.salesPrice:['min', self.get_q1, 'mean', 'median', 
                             self.get_q3, 'max','std', self.get_range,'skew']
        }).reset_index()

        names = ['FrequencySum','FrequencyMean','FrequencyMedian','FrequencyStd',
                 'MonetaryMin','MonetaryQ1','MonetaryMean','MonetaryMedian',
                 'MonetaryQ3','MonetaryMax','MonetaryStd','MonetaryRange','MonetarySkew']
        data.columns = [self.customerId] + [method +  name for name in names]

        denominator = {'year': 365, 'quarter':90, 'month': 30, 'week': 7}

        data.insert(loc=1, column=f'{method}Tenure', value=self.date_df['totalTenure'] / denominator[method])
        data.insert(loc=1, column=f'{method}Recency', value=self.date_df['totalRecency'] / denominator[method])

        return data

    def fit(self, data, method=None, snapshot=None):
        
        start = time.time()

        if snapshot == None:
            self.snapshot = data[self.orderDate].max() + np.timedelta64(1,'D')
        else:
            self.snapshot = pd.datetime(snapshot)
        
        rfmt_df = self.prep_rfmt(data)
        self.date_df = rfmt_df[['totalRecency','totalTenure']]
        method_dict = {'year':'year','yearQuarter':'quarter',
                       'yearMonth':'month','yearWeek':'week'}

        if method == None:
            rfmt_df = rfmt_df
        else:
            if method == 'year':
                columns = ['year']
            elif method == 'quarter':
                columns = ['yearQuarter']
            elif method == 'month':
                columns = ['yearMonth']
            elif method == 'week':
                columns = ['yearWeek']
            elif method == 'full':
                columns = ['year','yearQuarter','yearMonth','yearWeek']

            for enum, column in enumerate(columns):        
                rfmt_date = self.prep_rfmt_date(data, column, method_dict[column])
                rfmt_df = pd.concat([rfmt_df, rfmt_date.drop(self.customerId, axis=1)],axis=1)
        self.clear_cach
        print('successfully preped EzRFM {:.4f} ms'.format(time.time()-start))

        return rfmt_df.round(4)