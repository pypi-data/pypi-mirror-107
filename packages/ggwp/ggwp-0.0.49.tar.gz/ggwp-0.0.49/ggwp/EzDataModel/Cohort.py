import pandas as pd
import numpy as np
from datetime import datetime
import time

from ggwp.EzUtils.EzUtils import EzUtils

class Cohort(EzUtils):
    def __init__(self):
        super().__init__()
        self.data = 'EzCohort'
        self.basketDate = 'basketDate'
        self.customerId = 'customerId'
        self.orderId = 'orderId'
        self.orderDate = 'orderDate'
        self.salesPrice = 'salesPrice'
        self.cohortGrp = 'cohortGrp'
        self.cohortIdx = 'cohortIdx'
        self.frequency = 'frequency'

    @property
    def clear_cach(self):
        self.data = None

    @property
    def echo(self):
        print('EzCohort')

    def get_month(self, x):
        """
        return: datetime object
        """
        return datetime(x.year, x.month, 1)

    def get_date_int(self, column: str):
        """
        column <- column name containing invoice or order date
        return: tuple
        """
        series = pd.to_datetime(self.data[column])
        year = series.dt.year
        month = series.dt.month
        day = series.dt.day
        return year, month, day

    def get_cohort_index(self):
        basket_y, basket_m, basket_d = self.get_date_int(self.basketDate)
        cohort_y, cohort_m, cohort_d = self.get_date_int(self.cohortGrp)
        cohort_idx = (12*(basket_y - cohort_y) + (basket_m - cohort_m)) + 1
        self.data[self.cohortIdx] = cohort_idx

    def prep_cohort(self, data, method=None):
        self.data = data.copy()
        self.data[self.basketDate] = self.data[self.orderDate].apply(self.get_month)
        self.data = self.data.groupby([self.customerId, self.basketDate]).agg(
            frequency=pd.NamedAgg(column=self.orderId, aggfunc='nunique'),
            salesPrice=pd.NamedAgg(column=self.salesPrice, aggfunc='sum')
        ).reset_index()
        self.data[self.cohortGrp] = self.data.groupby(self.customerId)[self.basketDate].transform('min')
        self.get_cohort_index()
        self.data[self.customerId] = self.data[self.customerId].astype('object')
        return self.data

    def get_cohort_count(self):
        self.data = pd.pivot_table(self.data, index=self.cohortGrp,columns=self.cohortIdx, values=self.customerId, aggfunc='nunique')
        return self.data

    def get_cohort_retention(self):
        self.data = self.data.divide(self.data.iloc[:,0], axis=0)
        return self.data

    def get_cohort_sales(self):
        res = pd.pivot_table(self.data, index=self.cohortGrp,columns=self.cohortIdx, values=self.salesPrice, aggfunc='sum')
        return res

    def get_cohort_frequency(self):
        res = pd.pivot_table(self.data, index=self.cohortGrp,columns=self.cohortIdx, values=self.frequency, aggfunc='sum')
        return res

    def get_cohort_mean(self):
        total = self.get_cohort_sales()
        freq = self.get_cohort_frequency()
        self.data = total.divide(freq)
        return self.data

    def get_melt(self):
        self.data = self.data.reset_index()
        self.data = pd.melt(self.data, id_vars=self.cohortGrp)
        return self.data

    def fit(self, data, method='count', melt=False):
        """
        method = count, retention, sales, frequency, mean
        """
        start = time.time()
        self.prep_cohort(data, method=None)
        if method=='count':
            self.data = self.get_cohort_count()
        elif method=='retention':
            self.data = self.get_cohort_count()
            self.data = self.get_cohort_retention()
        elif method=='sales':
            self.data = self.get_cohort_sales()
        elif method=='frequency':
            self.data = self.get_cohort_frequency()
        elif method=='mean':
            self.get_cohort_mean()
        else:
            self.data = self.data

        if melt==True:
            self.get_melt()

        final_df = self.data
        
        self.clear_cach
        print('successfully preped EzCohort {:.4f} ms'.format(time.time()-start))

        return final_df.round(2)