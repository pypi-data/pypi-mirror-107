#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from torch.utils import data as pytorch_data

from dsframework.base_classes.object_base import ObjectBase
# from sigparser import SigparserPipeline
from dsframework.testable.sample import DatasetSample


class DatasetBase(ObjectBase, pytorch_data.Dataset):
    
    def __init__(self, name:str="dataset_base", path :str='', do_convert:bool=False, load_samples=False, defaults:dict={}, **kwargs):    
        ObjectBase.__init__(self, name, defaults,  **kwargs)
        # Default Init
        self.init_path(path)
        self.do_convert = do_convert
        self.load_samples = load_samples
        self.df_raw = None
        self.df     = None
        self.direct_samples_loading = False
        self.samples = []
        # Load dataframe or samples
        self.load_raw(path, load_samples)

    def populate(self):
        if self.do_convert:
            self.df, self.samples = self.convert()
        else:
            self.df = self.df_raw
            self.samples = self.build_samples()
            
    def build_samples(self):
        return [self.get_data_sample_from_row(self.df.iloc[i]) for i in range(len(self.df))]
    
    def load_raw(self, path='', load_samples=False):
        self.init_path(path)
        self.load_samples = load_samples
        self.direct_samples_loading = False
        if load_samples:
            self.samples = self.F.load_pickle(str(self.path))
            self.direct_samples_loading = True
        else:
            self.load(self.path)

    def build(self, path='', do_convert=False, load_samples=False):
        self.load_raw(path, load_samples)
        if not self.load_samples:
           self.populate()

    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        return self.samples[idx]

    def save(self, path=''):
        if '.json' in path:
            self.df.to_json(path, index=False)
        elif '.tsv' in path:
            self.df.to_csv(path, sep="\t", index=False)
        elif 'csv' in path:
            self.df.to_csv(path, index=False)
        self.F.save_pickle(self.df, path)

    def save_samples(self, path=''):
        self.F.save_pickle(self.samples, path)

    def load(self, dataset_path):
        dataset_path = str(dataset_path)
        if dataset_path.endswith('.csv'):
            self.df_raw = pd.read_csv(dataset_path)
        elif dataset_path.endswith('.json'):
            self.df_raw = pd.read_json(dataset_path)
        else:
            self.df_raw = self.F.load_pickle(dataset_path)

    def get_path(self, path=''):
        return self.path

    # IMPLEMENT IN SUPER CLASS
    def init_path(self, path):
        self.path = path
        return self.path

    def get_data_sample_from_row(self, row, i=None):
        features = {}
        len_row = len(row)
        if len_row>0:
            x = row.iloc[0]
        if len_row>1:
            y = row.iloc[-1]
        if len_row>2:
            features = row.iloc[1:-1].to_dict()
        return DatasetSample(x=x, y=y, features=features)

    def convert(self):
        return self.df, self.samples


# def get_data_sample_from_row_parallel(df_batch):
#     def get_sample_static(row, pipeline):
#         text = row.iloc[0]
#         gt_segments = row.iloc[1]
#         gt_segments_dict = literal_eval(gt_segments) if type(gt_segments) == str else gt_segments
#         pipeline_output = pipeline(text)
#         pred_segments = pipeline_output['signatures'][0]['segments']
#         pred_segments_dict = literal_eval(pred_segments) if type(pred_segments) == str else pred_segments
#         return DatasetSample(x=text, y=gt_segments_dict, pred=pred_segments_dict)
#
#     pipeline = SigparserPipeline()
#     l = []
#     total = len(df_batch)
#     for i in range(len(df_batch)):
#         l.append(get_sample_static(df_batch.iloc[i], pipeline))
#         prog = int((i/total)*100)
#         # print(prog)
#         if prog%10 == 0:
#             print(prog)
#     return l
#     # return [get_sample_static(df_batch.iloc[i], pipeline) for i in tqdm(range(len(df_batch)))]
