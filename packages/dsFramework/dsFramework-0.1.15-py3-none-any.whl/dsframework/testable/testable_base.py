
#!/usr/bin/env python
# coding: utf-8

from dsframework.base_classes.object_base import ObjectBase


class TestableBase(ObjectBase):
    def __init__(self, name:str="testable_base", defaults:dict={}, **kwargs):
        ObjectBase.__init__(self, name, defaults,  **kwargs)
        self.pipeline = None
        self.dataset = None
        self.reporter = None
        
    def init_pipeline(self, *args, **kwargs):
        raise NotImplementedError

    def init_dataset(self, path:str='', do_convert=False, load_samples=False, *args, **kwargs):
        raise NotImplementedError

    def init_reporter(self, *args, **kwargs):
        raise NotImplementedError
