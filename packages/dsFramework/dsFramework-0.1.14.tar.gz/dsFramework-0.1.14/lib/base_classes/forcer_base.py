from lib.base_classes.predictable_base import PredictableBase
from lib.base_classes.object_base import ObjectBase
from typing import List

from lib.shared.shared_objects import SharedArtifacts
from lib.config.zids_config import ZIDSConfig


class ForcerBase(ObjectBase):
    """
    Abstract class of forcer
    """

    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = "forcer_base", **kwargs):
        """
        :param config: configuration of module
        :param name: the name of component
        :param shared_artifacts: shared objects between pipeline parts
        :param str: the name of class (that will print in logger)
        :param kwargs: extra parameters of custom use
        """
        super(ForcerBase, self).__init__(config=config, shared_artifacts=shared_artifacts, name=name, **kwargs)

    def __call__(self, predictables_list: List[PredictableBase], **kwargs) -> List[PredictableBase]:
        """
        call function that run force function
        :param predictables_list: list of predictable objects for forcing
        :param kwargs: extra parameters
        :return: predictables objects after forcing
        """
        return self.force(predictables_list, **kwargs)

    def force(self, predictables_list: List[PredictableBase], **kwargs) -> List[PredictableBase]:
        """
        run forcing on list of predictable objects
        :param predictables_list: list of predictable objects
        :param kwargs: extra params
        :return: predictable objects after forcing
        """
        raise NotImplementedError
