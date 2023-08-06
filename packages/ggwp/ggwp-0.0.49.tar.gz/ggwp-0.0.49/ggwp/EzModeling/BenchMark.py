import pandas as pd
import numpy as np
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.svm import SVC
# from xgboost import XGBClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.dummy import DummyClassifier

from sklearn.linear_model import *
from sklearn.ensemble import *
from sklearn.svm import *
from xgboost import *
from sklearn.tree import *
from sklearn.dummy import *

from ggwp.EzModeling.Evaluation import Evaluation

class BenchMark(Evaluation): 
    def __init__(self):
        super().__init__()
        self.artifact_ = {}

    def get_single_line(self, X_train, y_train, X_test, y_test, remark, 
                        model_name, performance, artifact, method, id=None):
        row, col = X_train.shape
        
        columns = X_train.columns.to_list()
        
        idx = self.idx

        if method == 'add':
            id = self.id
            session = self.session
        elif method == 'update':
            id = int(id)
        single_line_df = pd.DataFrame(
            {
                'id':id,
                'session':session,
                'remark': remark,
                'model': model_name,
                'performance': [performance.to_dict()],
                'n_row':row,
                'n_col':col,
                'features': [columns],
                'X_train': [X_train.to_dict()],
                'y_train': [y_train.to_dict()],
                'X_test': [X_test.to_dict()],
                'y_test': [y_test.to_dict()],

            },
            index=[idx]
        )
        self.artifact_[id] = artifact

        return single_line_df

    def get_model(self, id):
        return self.artifact_[id]

    def add(self, X_train, y_train, X_test, y_test,
            model_name, performance, artifact, remark="nope"):        

        single_line_df = self.get_single_line(X_train, y_train, 
                                              X_test, y_test, remark=remark,
                                              model_name=model_name, performance=performance, 
                                              artifact=artifact, method='add', id=None)
        self.get_id('add')

        self.log = pd.concat([self.log,single_line_df],axis=0, ignore_index=True)
        return self.log

    def remove_session(self,session):
        if self.log.shape[0] == 1:
            self.log = pd.DataFrame()
        elif self.log.shape[0] > 1:
            self.log = self.log.loc[self.log['session'] != session]
            self.log.index = np.arange(self.log.shape[0])

        return self.log

    # *design logic first*
    # def update(self,data, remark="nope", id=None):
    #     single_line_df = self.get_single_line(data, remark, method='update', id=id)
    #     self.log.loc[self.log['id']==id] = single_line_df.values
        
    #     return self.log

    def train_model(self, X_train, y_train, X_test, y_test, model_dict, probability='target'):

        model_results = {}
        model_artifacts = {}
        for model_name, base_model in model_dict.items():

            print(f"start {model_name}")

            model = base_model
            model.fit(X_train,y_train)
            model_artifacts[model_name] = model
            probabilities = model.predict_proba(X_test)
            # if probability=='target':
            #     model_results[model_name] = probabilities[:,1]
            # elif probability=='all':
            #     model_results[model_name] = probabilities[:,:]

        # return model_artifacts, model_results
        return model_artifacts

    def benchmark(self, X_train, y_train, X_test, y_test, model_dict, remark, kind, cost, benefit):
        
        # model_artifacts, model_results  = self.train_model(X_train, y_train, X_test, y_test, model_dict)
        model_artifacts = self.train_model(X_train, y_train, X_test, y_test, model_dict)
        
        for model_name, artifact in model_artifacts.items():

            if kind == 'classification':
                performance = self.get_classification_report(model_name,y_test,artifact.predict_proba(X_test)[:,1],cost=cost,benefit=benefit)
            elif kind == 'regression':
                performance = self.get_regression_report(model_name,y_test,artifact.predict(X_test))

            self.add(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                 model_name=model_name, performance=performance, artifact=artifact, remark=remark)
            
        self.get_session(method='add')


    def classification_benchmark(self, X_train, y_train, X_test, y_test, model_dict, cost=0, benefit=0,remark='nope'):
        self.benchmark(X_train, y_train, X_test, y_test, model_dict, remark=remark, kind='classification', cost=cost, benefit=benefit)
        return self.log

    def regression_benchmark(self, X_train, y_train, X_test, y_test, model_dict, remark='nope'):    
        self.benchmark(X_train, y_train, X_test, y_test, model_dict, remark=remark, kind='regression')
        return self.log

    def get_data(self, id, kind='X_test'):
        if kind in ['X_train','X_test']:
            kind_df = pd.DataFrame(self.log.loc[self.log['id']==id, kind].values[0])
        elif kind in ['y_train','y_test']:
            kind_df = pd.Series(self.log.loc[self.log['id']==id, kind].values[0])
        return kind_df

    def get_performance(self, id):
        kind_df = pd.DataFrame(self.log.loc[self.log['id']==id, 'performance'].values[0])
        return kind_df

    def model_performance(self, id=None, session=None):
        
        if type(id) == int:
            id = [id]
        if type(session) == int:
            session = [session]

        if (id==None) & (session==None):
            performance_df = self.log.loc[:, ['id','session','performance']]
        elif (id==None) & (session!=None):
            performance_df = self.log.loc[self.log['session'].isin(session), ['id','session','performance']]
        elif (id!=None) & (session==None):
            performance_df = self.log.loc[self.log['id'].isin(id), ['id','session','performance']]
        else:
            performance_df = self.log.loc[(self.log['id'].isin(id)) & (self.log['session'].isin(session)), 
                                          ['id','session','performance']]

        ids = performance_df['id'].unique()
        final_df = pd.DataFrame()
        for id in ids:
            final_df = pd.concat([final_df,
                                  self.get_performance(id=id)],
                                 axis=0, ignore_index=True)
        return final_df