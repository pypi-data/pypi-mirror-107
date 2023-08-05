#!/usr/bin/env python
# coding: utf-8

from lib.testable.testable_base import TestableBase


class TesterBase(TestableBase):
    def __init__(self, name:str="tester_base", defaults:dict={}, **kwargs):
        TestableBase.__init__(self, name, defaults, **kwargs)
        self.report_df = None
        self.reporter = None
        self.report_col_names=[]
        self.report_header = ''
        self.report_path = ''
        self.reports = {}

    def set_report_header(self, report_header=''):
        self.report_header = report_header

    def set_report_path(self, report_path=''):
        self.report_path = report_path
        
    def test(self, prediction_path=None, **kwargs):
        pass

    def pre_test(self, **kwargs):
        pass

    def get_report_df_cols(self):
        if type(self.dataset.samples[0].y) is not dict:
            return ['cls_pred', 'cls_target', 'cls_prob', 'cls_tp', 'cls_fp', 'cls_tn', 'cls_fn']
        else:
            cols = []
            d = self.F.flatten(self.dataset.samples[0].y)
            for col_name in d:
                cols+= [f'{col_name}_pred', f'{col_name}_target',  f'{col_name}_prob'] + [f'{col_name}_tp', f'{col_name}_fp', f'{col_name}_tn', f'{col_name}_fn']
            return cols
    
    def evaluate(self, sample):
        def get_metrics(pred, target):
            TP = 1*all([pred, target, pred==target])
            FP = 1*all([pred, not target])
            TN = 1*all([not pred, not target])
            FN = 1*all([pred, target, pred!=target])
            return [TP, FP, TN, FN]

        out = []
        if type(sample.y) == dict:
            preds_dict  = self.F.flatten(sample.pred)
            target_dict = self.F.flatten(sample.y)
            for k, target in target_dict.items():
                pred = preds_dict[k] if k in preds_dict else ''
                out+= [pred, target, sample.prob] + get_metrics(pred, target)
        else:
            out+=[sample.pred, sample.y, sample.prob] + get_metrics(pred, target)
        return out
   

