from lib.testable.testable_base import TestableBase
from lib.testable.dataset_base import DatasetBase
import numpy as np

class TrainerBase(TestableBase):
    def __init__(self, name:str="trainer_base", defaults:dict={}, **kwargs):
        TestableBase.__init__(self, name, defaults, **kwargs)
        self.report_df = None
        self.reporter = None
        self.report_col_names=[]
        self.report_header = ''
        self.report_path = ''

    def set_report_header(self, report_header=''):
        self.report_header = report_header

    def set_report_path(self, report_path=''):
        self.report_path = report_path

    def pre_train(self):
        pass

    def train(self):
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
    
    def __build(self, dataset_path:str='', do_convert=False, report_path='', **kwargs):
        self.dataset = self.get_dataset(dataset_path, do_convert)
        self.set_report_path(report_path)
        self.report_df = None
        self.predictor = self.dataset.pipeline.labelize.predictor
        self.model     = self.predictor.get_new_model(**self.get_model_params_to_tune())

    def get_predictor_from_pipeline(self):
        return self.pipeline.labelize.predictor

    def get_model_from_pipeline(self):
        return self.pipeline.labelize.predictor.model

    def encode_using_pipeline(self, predictables):
        predictor = self.get_predictor_from_pipeline()
        encoded_features_dict_l = predictor.encode(predictables)
        X = []
        for features in encoded_features_dict_l:
            keys   = sorted(features.keys())
            values = [features[key] for key in keys]
            values = self.F.flatten_list(values)
            X.append(values)
        return np.array(X)
 
    def get_model_params_to_tune(self):
        return {}
        


    
   

