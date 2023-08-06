import pandas as pd
import numpy as np

from ggwp.EzModeling.Check import Check

class Log(Check):
    def __init__(self):
        super().__init__()
        self.log = pd.DataFrame()
        self.id = 1
        self.idx = 0
        self.session = 1

    def get_id(self, method):
        if method == 'add':
            self.id += 1

    def get_session(self, method):
        if method == 'add':
            self.session += 1

    def show(self):
        return self.log

    def detail(self, id):
        pass

    def get_single_line(self, data, remark, method, id=None):
        row, col = data.shape
        checked_data = self.check(data)
        data_dict = checked_data.to_dict()
        
        columns = checked_data.index.to_list()
        
        idx = self.idx

        if method == 'add':
            id = self.id
        elif method == 'update':
            id = int(id)
        single_line_df = pd.DataFrame(
            {
                'id':id,
                'remark': remark,
                'n_row':row,
                'n_col':col,
                'features': [columns],
                'data':[data.to_dict()]
            },
            index=[idx]
        )
        for k, v in data_dict.items():
            single_line_df[k] = pd.DataFrame({
                k:[v]
            },index=[idx])

        return single_line_df

    def add(self, data, remark="nope"):        
        single_line_df = self.get_single_line(data,remark, method='add')
        self.get_id('add')

        self.log = pd.concat([self.log,single_line_df],axis=0, ignore_index=True)
        return self.log

    def remove_id(self,id):
        if self.log.shape[0] == 1:
            self.log = pd.DataFrame()
        elif self.log.shape[0] > 1:
            self.log = self.log.loc[self.log['id'] != id]
            self.log.index = np.arange(self.log.shape[0])

        return self.log

    def update(self,data, remark="nope", id=None):
        single_line_df = self.get_single_line(data, remark, method='update', id=id)
        self.log.loc[self.log['id']==id] = single_line_df.values
        
        return self.log

    def get_detail(self, id):
        data = self.log.copy()
        filter = ['id', 'data','remark','n_row','n_col','features']
        data = data.loc[data['id']==id]
        row = data['n_row'].values[0]
        col = data['n_col'].values[0]
        remark = data['remark'].values[0]
        init = pd.DataFrame(index=data['features'].values[0])
        data = data.loc[:, ~data.columns.isin(filter)]

        for column in data.columns:
            init[column] = pd.Series(data[column].values[0])

        print(f"""remark: {remark}\nn_row, n_col: {row}, {col}""")

        return init

    def get_data(self, id):
        kind_df = pd.DataFrame(self.log.loc[self.log['id']==id, 'data'].values[0])
        return kind_df