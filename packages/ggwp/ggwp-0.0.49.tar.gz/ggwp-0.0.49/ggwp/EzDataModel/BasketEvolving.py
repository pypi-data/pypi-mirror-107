import pandas as pd
import numpy as np
from datetime import datetime
import time

from ggwp.EzUtils.EzUtils import EzUtils

class BasketEvolving(EzUtils):
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
        print("BasketEvolving")

    def prep_evolving(self, lags):
        evol_basket = self.data.copy()

        for lag in range(lags+1):
            column = '_{}'.format(lag)
            evol_basket[column] = evol_basket.groupby(self.customerId)[self.salesPrice].shift(lag).round(2)

        evol_basket = evol_basket.groupby(self.customerId).agg(
            {"_{}".format(i): lambda x: x.iloc[-1] for i in range(lags+1)}
        )

        evol_basket.columns = ['lag{}'.format(col) for col in evol_basket.columns]

        return evol_basket.reset_index().fillna(0)

    def prep_evolving_pct(self, lags):
        evol_basket = self.data.copy()

        for lag in range(lags+1):
            column = '_{}'.format(lag)
            evol_basket[column] = evol_basket.groupby(self.customerId)[self.salesPrice].pct_change(lag+1).round(2)

        evol_basket = evol_basket.groupby(self.customerId).agg(
            {"_{}".format(i): lambda x: x.iloc[-1] for i in range(lags+1)}
        )

        evol_basket.columns = ['pct{}'.format(col) for col in evol_basket.columns]

        return evol_basket.reset_index().fillna(0)

    def fit(self, data, lags=2):

        start = time.time()
        self.data = data
        evol_df = self.prep_evolving(lags=lags)
        evol_df_pct = self.prep_evolving_pct(lags=lags)

        final_df = evol_df.merge(evol_df_pct,how='left',left_on=self.customerId,right_on=self.customerId)
        self.clear_cach
        end = time.time()
        print('successfully preped BasketEvolving {:.4f} ms'.format(time.time()-start))      

        return final_df