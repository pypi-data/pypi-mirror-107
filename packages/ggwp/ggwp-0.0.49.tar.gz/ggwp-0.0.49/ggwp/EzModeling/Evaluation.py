from sklearn.metrics import (classification_report, confusion_matrix, plot_roc_curve,
                             accuracy_score, balanced_accuracy_score, 
                             recall_score, precision_score, f1_score, roc_auc_score,
                             mean_squared_error, mean_absolute_error, r2_score)
import pandas as pd
import numpy as np

from ggwp.EzModeling.Log import Log

import warnings
warnings.filterwarnings('ignore')

class Evaluation(Log):
    def __init__(self):
        super().__init__()

    def get_expected_value(self, cost, benefit):
        """
        This function will find the optimal cut-off ratio
        based on benefit and cost
        var:
            cost = cost occurs when the prediction is False Positive
            benefit = benefit occurs the prediction is True Positive
        return:
            the optimal cut-off ratio
        """
        return np.round(cost/benefit, 2)

    def cut_ratio(self, x,ratio=0.5):
        """
        This function will convert the probabilites to labels
        based on the cut-off ratio
        var:
            x = array of probability
            ratio = cut-off ratio (default = 0.5)
        return:
            array = array of labels (1 if x >= ratio else 0)
        """
        return np.where(x >= ratio,1,0)

    def get_confusion_matrix(self, y_true, y_pred): 
        """
        This function will convert y_true and y_pred to confusion_matrix
        based on the book titled "Data Science for Business" (p.200)
        var:
            y_true = actual labels
            y_pred = predicted labels
        result:
            confusion_matrix =
                column = actual
                row = predict
                            actual
                    positive | negative
                Yes |   (Y,p)  |   (Y,n)
                No  |   (N,p)  |   (N,n)
        """
        return confusion_matrix(y_true,y_pred).T[::-1,::-1]

    def get_confusion_rate(self, x):
        """
        This function will convert confusion_matrix to confusion_rate
        var:
            x = confusion_matrix
        return:
            confusion_rate
        """
        return x/x.sum(axis=0)

    def get_prior(self, x):
        """
        This function will extract the class prior rate from confusion_matrix
        var:
            x = confusion_matrix
        return:
            prior_matrix
        """
        x = x.sum(axis=0)/x.sum()
        x = np.array([x,x])
        return x

    def expected_values(self, conf_mat, cost, benefit,n_round=2):
        """
        This function will get the expected values from confusion_matrix and cost_benefit_matrix
        var:
            conf_mat = confusion_matrix
            cost_benefit = cost_benefit_matrix
            n_round = round number (default = return 2 decimal)
        return:
            expected_values from the confusion_matrix in scalar
        """
        cost_benefit = np.array([
                                [0,0],
                                [0,0]
        ])
        cost_benefit[0,0] = benefit
        cost_benefit[0,1] = -1*cost
        conf_r = self.get_confusion_rate(conf_mat)
        conf_p = self.get_prior(conf_mat)
        res = conf_r.round(n_round) * cost_benefit * conf_p.round(n_round)
        return res.sum().round(n_round)

    def get_roc(self, x):
        """
        This function will get True Positive and False Positive rates from confusion_matrix
        var:
            x = confusion_matrix
        return:
            True Positive and False Positive rate in tuple
        """
        true_pos, false_pos = x[0,:]/x.sum(axis=0)
        return true_pos, false_pos

    def get_classification_report(self, model_name,y_true,y_pred,cost=0,benefit=0,round_n=4):
        """
        This function will generate the dataframe 
        containing essential values for evaluation
        var:
            y_true = actual labels
            y_pred = predicted probabilities
            cost = cost
            benefit = benefit
            round_n = round number (default = .4 decimal)
        return:
            dataframe with columns:
                ratio = cut-off ratio
                p_samples = sum of True Positive and False Positive
                pct_samples = sample ratio calculated by p_samples/the total samples
                profit = expected_values of the cut-off
                tp = True Positive rate
                fp = False Positive rate
                auc = area under the ROC curve
                lift = lift value calculated by (tp*100)/pct_samples
                model = the model's name
        """
        cut_off_list = []
        predicted_positive_list = []
        positive_pct_list =[]
        cost_benefit_list = []
        tp_list = []
        fp_list = []
        acc_list = []
        acc_balanced_list = []
        recall_list = []
        precision_list = []
        f1_list = []
        f1_weighted_list = []
        auc_list = []

        for i in range(100):
            ratio_n = i/100
            cut_off_list.append(ratio_n)
            y_prob = self.cut_ratio(y_pred,ratio_n)
            conf_m = self.get_confusion_matrix(y_true,y_prob)

            tp, fp = self.get_roc(conf_m)      
            tp_list.append(tp.round(round_n))
            fp_list.append(fp.round(round_n))
            positive_samples = conf_m[0].sum()
            positive_pct = positive_samples/conf_m.sum().sum()
            predicted_positive_list.append(positive_samples)
            positive_pct_list.append(positive_pct.round(round_n))
            cost_benefit_list.append(self.expected_values(conf_m, cost=cost, benefit=benefit))

            acc_list.append(accuracy_score(y_true, y_prob))
            acc_balanced_list.append(balanced_accuracy_score(y_true, y_prob))
            precision_list.append(precision_score(y_true, y_prob))
            recall_list.append(recall_score(y_true, y_prob))
            f1_list.append(f1_score(y_true, y_prob))
            f1_weighted_list.append(f1_score(y_true, y_prob, average='weighted'))
            auc_list.append(roc_auc_score(y_true,y_prob))

        prof_df = pd.DataFrame({'ratio':cut_off_list,
                                'p_samples':predicted_positive_list,
                                'pct_samples':positive_pct_list,
                                'profit':cost_benefit_list,
                                'tp':tp_list,
                                'fp':fp_list,
                                'acc':acc_list,
                                'acc_balanced':acc_balanced_list,
                                'precision': precision_list,
                                'recall': recall_list,
                                'f1':f1_list,
                                'f1_weighted':f1_weighted_list,
                                'auc':auc_list
                                })
        # prof_df['auc'] = auc.round(round_n)
        # prof_df['lift'] = (prof_df['tp']*100)/prof_df['pct_samples']
        prof_df['lift'] = (prof_df['tp'])/prof_df['pct_samples']
        # prof_df['model'] = model_name
        prof_df.insert(loc=0, column='model', value=model_name)
        prof_df.insert(loc=0, column='session', value=self.session)
        prof_df.insert(loc=0, column='id', value=self.id)
        prof_df.insert(loc=3, column='id_model', value='id ' + prof_df['id'].astype(str) + ": " + prof_df['model'])
        # prof_df['id_model'] = 'id ' + prof_df['id'].astype(str) + ": " + prof_df['model']
        return prof_df.round(round_n)

#----------

    def get_regression_report(self, model_name,y_true,y_pred,round_n=4):

        r2_list = []
        rmse_list = []
        mse_list = []
        mae_list =[]
        
        for i in range(100):

            r2_list.append(r2_score(y_true, y_pred))
            rmse_list.append(mean_squared_error(y_true, y_pred, squared=True))
            mse_list.append(mean_squared_error(y_true, y_pred, squared=False))
            mae_list.append(mean_absolute_error(y_true, y_pred))

        prof_df = pd.DataFrame({
            'r2':r2_list,
            'rmse':rmse_list,
            'mse':mse_list,
            'mae':mae_list
                                })

        prof_df.insert(loc=0, column='model', value=model_name)
        prof_df.insert(loc=0, column='session', value=self.session)
        prof_df.insert(loc=0, column='id', value=self.id)
        prof_df.insert(loc=3, column='id_model', value='id ' + prof_df['id'].astype(str) + ": " + prof_df['model'])

        return prof_df.round(round_n)

    def get_profit_all_models(self, y_test, model_dict, cost=0, benefit=0):
        prof_all = pd.DataFrame()
        for model_name, model in model_artifacts.items():
            prof_all = pd.concat([prof_all,
                                  self.get_classification_report(model_name=model_name, y_true=y_test,
                                                        y_pred=model.predict_proba(X_test)[:,1],
                                                        cost=cost,benefit=benefit,round_n=4)
                                  ], axis=0, ignore_index=True)


        return prof_all

    # not used for now
    def get_report(self, X, y_true, y_pred, method):
        if method == 'classsification':
            report = self.get_classification_report(y_true, y_pred)

        elif method == 'regression':
            report = self.get_regression_report(y_true, y_pred)