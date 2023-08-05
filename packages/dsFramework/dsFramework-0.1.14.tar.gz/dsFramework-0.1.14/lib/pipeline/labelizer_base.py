from typing import List

from lib.base_classes.predictable_base import PredictableBase
from lib.base_classes.predictor_base import PredictorBase
from lib.base_classes.forcer_base import ForcerBase
from lib.base_classes.object_base import ObjectBase
from lib.shared.shared_objects import SharedArtifacts
from lib.config.zids_config import ZIDSConfig


class LabelizerBase(ObjectBase):
    """
    Abstract class of labelizer component
    """

    def __init__(self, name: str = "labelizer_base", config: ZIDSConfig = None, shared_artifacts: SharedArtifacts = None,
                 **kwargs):
        super(LabelizerBase, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)
        self.model_path = self.config.get('model_path')
        self.use_dummy_model = self.config.get('use_dummy_model')
        self.threshold = self.config.get('threshold')
        self.forcer = None
        self.predictor = None
        self.predictable_l = []
        self.set_predictor()
        self.set_forcer()

    def __call__(self, predictable_l: List[PredictableBase]) -> List[PredictableBase]:
        return self.labelize(predictable_l)

    def set_predictor(self, predictor: PredictorBase = None):
        """
        set the predictor
        :param predictor: the predictor
        """
        if not predictor:
            self.init_predictor(self.config, self.shared_objects)
        else:
            self.predictor = predictor

    def set_forcer(self, forcer: ForcerBase = None):
        """
        set forcer
        :param forcer: the forcer
        """
        if not forcer:
            self.init_forcer(config=self.config, shared_objects=self.shared_objects)
        else:
            self.forcer = forcer

    def init_predictor(self, config: ZIDSConfig, shared_objects: SharedArtifacts):
        """
        init predictor
        """
        raise NotImplementedError

    def init_forcer(self, config: ZIDSConfig, shared_objects: SharedArtifacts):
        """
        init forcer
        """
        raise NotImplementedError

    def reset(self, predictable_l: List[PredictableBase], **kwargs):
        """
        reset the class members
        :param predictable_l: list of predictable objects to labelize
        :return: predictable list after labeling and forcing
        """
        if predictable_l is None:
            predictable_l = []
        self.predictable_l = predictable_l
        if not self.predictable_l:
            return False
        if not self.predictor:
            self.set_predictor()
        if not self.forcer:
            self.set_forcer()
        return True

    def labelize(self, predictable_l: List[PredictableBase]):
        """
        lablize each predictable object
        :param predictable_l: list of predictable objects to labelize
        """
        if predictable_l is None:
            predictable_l = []
        if self.reset(predictable_l):
            self.predictor(self.predictable_l)
            self.forcer(self.predictable_l)
