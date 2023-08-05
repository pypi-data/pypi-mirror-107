#!/usr/bin/env python
# coding: utf-8
from typing import Dict, Any, List

from dsframework.base_classes.predictable_base import PredictableBase
from dsframework.shared.shared_objects import SharedArtifacts
from dsframework.base_classes.object_base import ObjectBase
from dsframework.config.zids_config import ZIDSConfig


class PostprocessorBase(ObjectBase):
    """
    Abstract postprocessor class
    """
    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = "postprocess_base", **kwargs):
        super(PostprocessorBase, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)

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
