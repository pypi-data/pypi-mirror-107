#!/usr/bin/env python
# coding: utf-8

from dsframework.base_classes.object_base import ObjectBase

class DatasetSample(ObjectBase):
    def __init__(self, name='dataset_sample', x=None, y=None, features=None, pred=-1, prob=-1, **kwargs):
        ObjectBase.__init__(self, name, {}, **kwargs)
        self.reset(x, y, features, pred, prob)
    
    def reset(self, x=None, y=None, features=None, pred=-1, prob=-1, forced_reason='', orig_prediction=-1):
        self.x = x
        self.y = y
        self.features = features
        self.pred = pred
        self.prob = prob
        self.forced_reason = forced_reason
        self.orig_prediction = orig_prediction
