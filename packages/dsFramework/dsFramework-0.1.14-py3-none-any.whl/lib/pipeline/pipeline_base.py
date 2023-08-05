#!/usr/bin/env python
# coding: utf-8
import yaml

from lib.shared.shared_objects import SharedArtifacts
from lib.config.zids_config import ZIDSConfig
from typing import Dict, Any
from lib import functions as F


class PipelineBase:
    """
    Abstract class of pipeline
    """
    def __init__(self, config_path: str = '', **kwargs):
        self.configs = self.read_config(config_path=config_path)
        self.inputs = None
        self.preprocess = None
        self.labelize = None
        self.postprocess = None
        self.shared_memory = SharedArtifacts()
        self.vocab_path = self.configs['pipeline'].get('vocab_path')
        self.vocabs_to_load = self.configs['pipeline'].get('vocabs_to_load')
        self.scalers_path = self.configs['pipeline'].get('scalers_path')
        self.scalers_to_load = self.configs['pipeline'].get('scalers_to_load')
        self.__build()

    def __build(self):
        self.load_shared_objects()
        self.init_preprocessor(config=self.configs['preprocessor'], shared_object=self.shared_memory)
        self.init_labelizer(config=self.configs['labelizer'], shared_object=self.shared_memory)
        self.init_postprocessor(config=self.configs['postprocessor'], shared_object=self.shared_memory)

    def load_shared_objects(self) -> None:
        """
        load shared object between all component in pipeline
        """
        self.load_gazetteer()
        self.load_scalers()

    def load_gazetteer(self) -> None:
        """
        load gazetteers
        """
        for vocab_filename, vocab_name, vocab_type in self.vocabs_to_load:
            path = self.vocab_path + '/' + vocab_filename
            vocab = F.load_json(path) if vocab_type == 'json' else F.load_pickle(path)
            if type(vocab) == dict and type(vocab[list(vocab.keys())[0]]) == dict:
                for vocab_name_in_dict in vocab.keys():
                    self.shared_memory.save_object(vocab_name_in_dict, vocab[vocab_name_in_dict])
            else:
                self.shared_memory.save_object(vocab_name, vocab)

    def load_scalers(self) -> None:
        """
        load scalers
        """
        for scaler_name, scaler_filename in self.scalers_to_load:
            path = self.scalers_path + '/' + scaler_filename
            scaler = F.load_pickle(path)
            self.shared_memory.save_object(scaler_name, scaler)

    def reset(self, **inputs) -> None:
        """
        assign the inputs into class members
        :param inputs: the inputs
        """
        self.inputs = inputs

    def __call__(self, **inputs):
        return self.run(**inputs)

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        run the pipeline
        :param kwargs: inputs
        :return: dict of results
        """
        self.reset(**kwargs)
        predictables = self.preprocess(**self.inputs)
        self.labelize(predictables)
        return self.postprocess(predictables)

    def init_preprocessor(self, config: ZIDSConfig, shared_object: SharedArtifacts) -> None:
        """
        abstract method to init the preprocessor
        :param config: config object
        :param shared_object: shared object between pipeline component
        """
        self.preprocess = None
        raise NotImplementedError

    def init_labelizer(self, config: ZIDSConfig, shared_object: SharedArtifacts) -> None:
        """
        abstract method to init labelizer
        :param config: config object
        :param shared_object: shared object between pipeline component
        """
        self.labelize = None
        raise NotImplementedError

    def init_postprocessor(self, config: ZIDSConfig, shared_object: SharedArtifacts) -> None:
        """
        abstract method to init postprocessor
        :param config: config object
        :param shared_object: shared object between pipeline component
        """
        self.postprocess = None
        raise NotImplementedError

    @staticmethod
    def read_config(config_path: str = '') -> Dict[str, ZIDSConfig]:
        """
        read configuration from yaml file
        :param config_path: configuration path
        :return:
        """
        with open(config_path, 'r') as yaml_file:
            cfg = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return {component: ZIDSConfig(cfg[component])
                for component in ['pipeline', 'preprocessor', 'labelizer', 'postprocessor']}
