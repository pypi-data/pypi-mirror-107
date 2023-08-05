import yaml
from typing import Dict
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

from dsframework.pipeline import PipelineBase
from dsframework.config import ZIDSConfig
from dsframework.shared import SharedArtifacts
from dsframework.utils.registry import Registry
from generatedDirectory.preprocessor import generatedProjectNamePreprocessor
from generatedDirectory.labelizer import generatedProjectNameLabelizer
from generatedDirectory.postprocessor import generatedProjectNamePostprocessor

class generatedClass(PipelineBase):
    @staticmethod
    def getInstance(name = 'generatedDirectory', **kwargs):
        # generatedDirectory =  Registry.initialize(name, None, generatedClass)
        # generatedDirectory.cfg.update(generatedDirectory.name, kwargs)
        return generatedClass

    def __init__(self, config_path: str = 'config.yaml', **kwargs):
        super(generatedClass, self).__init__(name="generatedClassName", config_path=config_path,**kwargs)
    def __call__(self, url: str = '', html: str = '', link_text: str = '', **kwargs):
        return PipelineBase.__call__(self, url=url, html=html, link_text=link_text, **kwargs)

    def init_preprocessor(self, config: ZIDSConfig, shared_object: SharedArtifacts):
        self.preprocess = generatedProjectNamePreprocessor(config=config, shared_artifacts=shared_object)
        return self.preprocess

    def init_labelizer(self, config: ZIDSConfig, shared_object: SharedArtifacts = None):
        self.labelize = generatedProjectNameLabelizer(config=config, shared_artifacts=shared_object)
        return self.labelize

    def init_postprocessor(self, config: ZIDSConfig, shared_object: SharedArtifacts = None):
        self.postprocess = generatedProjectNamePostprocessor(config=config, shared_artifacts=shared_object)
        return self.postprocess

    @staticmethod
    def read_config(config_path: str = '') -> Dict[str, ZIDSConfig]:
        """
        read configuration from yaml file
        :param config_path: configuration path
        :return:
        """
        with open(os.path.join(__location__, config_path), 'r') as yaml_file:
            cfg = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return {component: ZIDSConfig(cfg[component])
                for component in ['pipeline', 'preprocessor', 'labelizer', 'postprocessor']}
