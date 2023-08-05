from typing import Dict, Any, List
from dsframework.pipeline import PreprocessorBase
from dsframework.config import ZIDSConfig
from dsframework.shared import SharedArtifacts
from dsframework.base_classes import PredictableBase

class generatedClass(PreprocessorBase):
    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = 'generatedClassName',
                 **kwargs):
        super(generatedClass, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)

    def __call__(self, **kwargs) -> PredictableBase:
        raise NotImplementedError

    def get_empty_final_output(self) -> Dict[str, Any]:
        """
        create template of output
        """
        raise NotImplementedError

    def preprocess(self, obj_list: List[Any], **kwargs) -> Dict[str, Any]:
        """
        create output
        :param obj_list: list of objects
        :param kwargs: extra params
        """
        raise NotImplementedError
