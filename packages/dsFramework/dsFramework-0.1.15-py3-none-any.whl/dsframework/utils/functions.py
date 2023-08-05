from dsframework.utils import RegexHandler
from datetime import datetime
import pickle
import json
import os

regex = RegexHandler


def flatten(d, sep="_"):
    import collections

    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):

        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)

    return obj


def get_from_dict(key, container: dict, default='', delete=False):
    if not container or type(container) is not dict:
        return default
    if key in container:
        val = container[key]
        if delete:
            del container[key]
        return val
    return default


def get_date_time(short=False):
    now = datetime.now()
    form = '%d/%m/%Y %H:%M:%S' if not short else '%d_%m_%Y'
    dt_string = now.strftime(form)
    return dt_string


def load_pickle(path):
    pkl = None
    if os.path.exists(path):
        with open(path, 'rb') as fid:
            pkl = pickle.load(fid)
    return pkl


def load_json(path):
    jsn = None
    with open(path) as fid:
        jsn = json.load(fid)
    return jsn


def save_pickle(obj, path):
    with open(path, 'wb') as fid:
        pickle.dump(obj, fid)


def save_json(obj, path):
    with open(path, 'w') as f:
        json.dump(f, obj)


def remove_empty_leafs(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (remove_empty_leafs(v) for v in d) if v]
    return {k: v for k, v in ((k, remove_empty_leafs(v)) for k, v in d.items()) if v}


def flatten_list(l):
    def get_el(el):
        if type(el) is not list:
            return [el]
        return el

    l2 = [get_el(el) for el in l]
    flatten = lambda l: [item for sublist in l for item in sublist]
    return flatten(l2)


def is_list_of_list(l):
    for el in l:
        if type(el) is list:
            return True
    return False


def get_html_block_elements_list():
    return ['<address', '<article', '<aside', '<blockquote', '<canvas', '<dd', '<div',
            '<dl',
            '<dt', '<fieldset', '<figcaption', '<figure', '<footer', '<form', '<h1',
            '<h2', '<h3',
            '<h4', '<h5', '<h6', '<header', '<hr', '<li', '<main', '<nav',
            '<noscript', '<ol', '<p', '<pre', '<section', '<table', '<tfoot', '<ul',
            '<video']


def get_html_inline_elements_list():
    return ['<a', '<abbr', '<acronym', '<b', '<bdo', '<big', '<br', '<button', '<cite',
            '<code', '<dfn', '<em',
            '<i', '<img', '<input', '<kbd', '<label', '<map', '<object', '<output',
            '<q', '<samp', '<script',
            '<select', '<small', '<span', '<strong', '<sub', '<sup', '<textarea',
            '<time', '<tt', '<var']
