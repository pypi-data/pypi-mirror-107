from typing import Dict, Any, List
from dsFramework import PostprocessorBase, ZIDSConfig, SharedArtifacts
from dsFramework.base_classes import PredictableBase

class generatedClass(PostprocessorBase):
    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = 'generatedClassName',
                 **kwargs):
        super(generatedClass, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)

    def __call__(self, predictable_obj=None, **kwargs):
        return self.postprocess(predictable_obj, **kwargs)

    def get_empty_final_output(self) -> Dict[str, Any]:
        """
        create template of output
        """
        raise NotImplementedError

    def postprocess(self, predictable_obj_list: List[PredictableBase], **kwargs) -> Dict[str, Any]:
        """
        create output
        :param predictable_obj_list: list of predictable objects
        :param kwargs: extra params
        """
        raise NotImplementedError
