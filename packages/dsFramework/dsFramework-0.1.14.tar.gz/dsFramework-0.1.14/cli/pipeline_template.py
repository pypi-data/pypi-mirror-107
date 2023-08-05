from dsFramework import PipelineBase, ZIDSConfig, SharedArtifacts
from generatedDirectory.preprocessor import generatedProjectNamePreprocessor
from generatedDirectory.labelizer import generatedProjectNameLabelizer
from generatedDirectory.postprocessor import generatedProjectNamePostprocessor

class generatedClass(PipelineBase):
    def __init__(self, config_path: str = '', **kwargs):
        super(generatedClass, self).__init__(name="generatedClassName", config_path=config_path,
                                                         **kwargs)
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
