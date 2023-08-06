import pandas as pd
import numpy as np
from datetime import datetime
import time

from ggwp.EzUtils.EzUtils import EzUtils

class DataModel(EzUtils):
    def __init__(self):
        super().__init__()
        self.data = None
        self.customerId = 'customerId'
        self.orderId = 'orderId'
        self.orderDate = 'orderDate'
        self.salesPrice = 'salesPrice'

    @property
    def clear_cach(self):
        self.data = None

    @property
    def echo(self):
        print('DataModel')

    def get_range(self, x):
        return x.max()-x.min()

    def get_q1(self, x):
        return x.quantile(.25)

    def get_q3(self, x):
        return x.quantile(.75)

    def convert_dtypes(self):
        convert_dict = {'object':['customerId','orderId'],
                        'float':'salesPrice'}
        for datatype, col in convert_dict.items():
            self.data[col] = self.data[col].astype(datatype)

    def make_date_normal(self):
        self.data['date'] = self.data[self.orderDate].dt.date
        self.data['year'] = self.data[self.orderDate].dt.year
        self.data['quarter'] = self.data[self.orderDate].dt.quarter
        self.data['month'] = self.data[self.orderDate].dt.month
        self.data['week'] = self.data[self.orderDate].dt.isocalendar().week
        self.data['day'] = self.data[self.orderDate].dt.day
        self.data['dayOfYear'] = self.data[self.orderDate].dt.dayofyear

    def make_date_combined(self):
        self.data['yearQuarter'] = self.data['year'].astype(str)+'-'+self.data['quarter'].astype(str)
        self.data['yearMonth'] = self.data['year'].astype(str)+'-'+self.data['month'].astype(str).apply(lambda x: x.zfill(2))
        self.data['yearWeek'] = self.data['year'].astype(str)+'-'+self.data['week'].astype(str).apply(lambda x: x.zfill(2))
        self.data['yearDay'] = self.data['year'].astype(str)+'-'+self.data['day'].astype(str).apply(lambda x: x.zfill(2))
        self.data['yearDayYear'] = self.data['year'].astype(str)+'-'+self.data['dayOfYear'].astype(str).apply(lambda x: x.zfill(3))

    def get_date(self, date):

        combined_col = ['customerId', 'orderId', 'salesPrice', 'orderDate', 'yearQuarter',
       'yearMonth', 'yearWeek', 'yearDay', 'yearDayYear']

        if date == 'normal':
            self.make_date_normal()
        elif date == 'combined':
            self.make_date_combined()
            self.data[combined_col] = self.data[combined_col]
        elif date == 'full':
            self.make_date_normal()
            self.make_date_combined()
        else:
            pass

    def aggregate(self, data, customerId, orderId, orderDate, salesPrice):
        self.data = data.groupby([customerId,orderId]).agg(
            salesPrice = pd.NamedAgg(column=salesPrice, aggfunc='sum'),
            orderDate = pd.NamedAgg(column=orderDate, aggfunc=lambda x: x.iloc[-1]),
        ).reset_index()
        self.data.rename(columns={customerId:self.customerId,orderId:self.orderId},inplace=True)

    def prep(self, data, customerId, orderId, orderDate, salesPrice, date='full', method=None):
        """
        method = yqmwd, yq, ym, yw, yd
        """
        start = time.time()
        self.aggregate(data, customerId, orderId, orderDate, salesPrice)
        self.get_date(date)
        self.convert_dtypes()
        final_df = self.data.copy()
        self.clear_cach
        print('successfully preped DataModel {:.4f} ms'.format(time.time()-start))

        for col, map in zip([customerId, orderId, orderDate, salesPrice],
                            [self.customerId, self.orderId, self.orderDate, self.salesPrice]):
            print(f"Changed from {col} to {map}")

        return final_df