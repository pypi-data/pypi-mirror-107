import pandas as pd
import numpy as np
from datetime import datetime
import time
# from .DataModel import DataModel
from ggwp.EzDataModel.Cohort import Cohort

class CustomerMovement(Cohort):
    def __init__(self):
        super().__init__()
        self.data = 'EzCustomerMovement'

    @property
    def clear_cach(self):
        self.data = None

    @property
    def echo(self):
        print('EzCustomerMovement')

    def status_code(self, x):
        if x == 0:
            return 'new'
        elif x == 1:
            return 'repeat'
        elif x > 1:
            return 'reactivate'

    def get_status(self):
        self.data['shift'] = self.data.groupby('customerId')[self.cohortIdx].shift(1).fillna(1).astype('int')
        self.data['statusId'] = self.data[self.cohortIdx] - self.data['shift']
        self.data['status'] = self.data['statusId'].apply(self.status_code)

    def get_churn(self):
        self.data = pd.pivot_table(self.data, 
                                        index=self.basketDate,columns='status',values='customerId',
                                        aggfunc='count',fill_value=0)
        self.data['not_new'] = self.data['reactivate'] + self.data['repeat']
        self.data['cumsum'] = self.data['new'].cumsum().fillna(0)
        self.data['churn'] = self.data['new'] + self.data['not_new']-self.data['cumsum']
        self.data = self.data.reset_index()    

    def prep_customer_movement(self, data):
        self.data = self.prep_cohort(data)
        self.get_status()
        self.get_churn()
        return self.data

    def get_melt(self):
        self.data = pd.melt(self.data, id_vars=self.basketDate)
        return self.data

    def fit(self, data, method=None, melt=True):
        """
        method = normal, melt
        """
        start = time.time()
        columns = [self.basketDate,'new','reactivate','repeat','churn']
        self.data = self.prep_customer_movement(data)[columns]
        
        if melt==True:
            self.data = self.get_melt()

        final_df = self.data
        
        self.clear_cach
        print('successfully preped EzCustomerMovement{:.4f} ms'.format(time.time()-start))
        return final_df