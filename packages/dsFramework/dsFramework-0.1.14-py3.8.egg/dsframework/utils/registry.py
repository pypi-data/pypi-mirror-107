#!/usr/bin/env python
# coding: utf-8

class RegistryBase:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)
            
    def register(self, key, value):
        self.__setattr__(key, value)
    
    def get(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return None
        
    def __setattr__(self, name, value):
          self.__dict__[name] = value
            
    def __getattr__(self, name):
        return None

class Registry:
    base = RegistryBase()
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            Registry.base.__setattr__(k, v)
    
    @staticmethod        
    def register(key, value):
        Registry.base.__setattr__(key, value)
    
    @staticmethod        
    def clear(key):
        if Registry.has(key):
            del Registry.base.__dict__[key]

    @staticmethod
    def get(key, dflt = None):
        if key in Registry.base.__dict__:
            return Registry.base.__dict__[key]
        else:
            if dflt is not None:
                Registry.register(key, dflt)
                return Registry.get(key)
            return dflt
    
    @staticmethod
    def list_all():
        for key in Registry.base.__dict__:
            print(key)
    
    @staticmethod
    def has(attr):
        return attr in Registry.base.__dict__

    @staticmethod
    def initialize(key, obj, cls):
        if isinstance(obj, cls):
            return obj
        else:
            o = Registry.get(key)
            if not isinstance(o, cls):
                o = cls()
                Registry.register(key, o)
            return o