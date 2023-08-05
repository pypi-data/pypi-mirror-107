"""
Preprocess component that create predictable objects
"""
from lib.base_classes.predictable_base import PredictableBase
from lib.shared.shared_objects import SharedArtifacts
from lib.base_classes.object_base import ObjectBase
from lib.config.zids_config import ZIDSConfig


class PreprocessorBase(ObjectBase):
    """
    Preprocess component that create predictable objects
    """

    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = "preprocess_base", **kwargs):
        super(PreprocessorBase, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)

    def __call__(self, **kwargs) -> PredictableBase:
        raise NotImplementedError
