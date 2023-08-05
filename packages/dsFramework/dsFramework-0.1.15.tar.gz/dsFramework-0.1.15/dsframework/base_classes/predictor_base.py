"""
The abstract class for predictor component
"""
from typing import Any, List, Tuple, Dict

import numpy as np

from dsframework.base_classes.predictable_base import PredictableBase
from dsframework.shared.shared_objects import SharedArtifacts
from dsframework.config.zids_config import ZIDSConfig
from dsframework.utils import functions as F
from dsframework.base_classes.object_base import ObjectBase


class PredictorBase(ObjectBase):
    """
    The abstract class for predictor component
    """

    def __init__(self, name: str = "predictor_base", model_path: str = '', use_dummy_model: bool = False,
                 threshold: float = 0.5, shared_artifacts: SharedArtifacts = None, config: ZIDSConfig = None, **kwargs):
        super(PredictorBase, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)
        self.model_path = model_path
        self.use_dummy_model = use_dummy_model
        self.threshold = threshold
        self.__build()

    def __build(self):
        self.model_reset()
        self.reset()
        self.load_model()

    def model_reset(self):
        """
        function to reset model
        """
        self.loaded = False
        self.model = None

    def reset(self):
        """
        reset the encoded features
        """
        self.encoded_features = []

    def __call__(self, candidate=None):
        return self.run_predict(candidate)

    def save_model(self):
        """
        save model to file
        """
        if self.loaded:
            path = self.init_model_path()
            F.save_pickle(self.model, path)

    def load_model(self):
        """
        load model from file
        """
        path = self.init_model_path()
        if path and not self.use_dummy_model:
            self.model = F.load_pickle(path)
            self.loaded = True
        else:
            self.loaded = False

    def get_model(self, new=False, **model_params):
        """
        get model instance
        :param new: new model or old
        :param model_params: parameters for model
        :return: model instance
        """
        if new or not self.model:
            return self.init_new_model(**model_params)
        return self.model

    def encode(self, predictables=None):
        """
        convert predictable objects into encoded features
        :param predictables: list of predictable objects
        :return: list of encoded features
        """
        if predictables is None:
            predictables = []
        self.reset()
        for predictable in predictables:
            self.encoded_features.append(self.encode_attributes(predictable.get_attributes()))
        return self.encoded_features

    @staticmethod
    def features_to_np_array(features_list: List[Any]):
        """
        convert feautres to ndarray
        :param features_list: list of features
        :return: ndarray
        """
        if features_list is None:
            features_list = []
        X_np = np.array(features_list)
        return X_np

    def run_predict(self, predictables: List[PredictableBase]) -> Tuple[
        List[float], List[float], List[PredictableBase]]:
        """
        run predict
        :param predictables: list of predictable object
        :return: the
        """
        if predictables is None:
            predictables = []
        if type(predictables) is not list:
            predictables = [predictables]
        if not predictables:
            preds = []
            probs = []
        elif self.use_dummy_model:
            preds = [0] * len(predictables)
            probs = [-1] * len(predictables)
        else:
            if not self.loaded and not self.use_dummy_model:
                self.load_model()
            preds, probs = self.predict(self.encode(predictables))
        return self.post_predict(preds, probs, predictables)

    # IMPLEMENT IN SUPER CLASS

    def init_new_model(self, **model_params) -> Any:
        """
        return new model instance with given params
        :param model_params: model parameters
        :return: model instance with parameters
        """
        self.model = None
        return self.model

    def init_model_path(self, path: str = None) -> str:
        """
        init the model path
        :param path: the given path
        :return: return if path is not None return path else self.model_path
        """
        raise NotImplementedError

    @staticmethod
    def encode_attributes(attributes: dict) -> Dict[str, Any]:
        """
        return encoding attributes -> conf
        :param attributes:
        :return: return dict with only numeric values
        """
        if attributes is None:
            attributes = {}
        return attributes

    def predict(self, features_list: Dict[str, List[float]]) -> Tuple[List[float], List[float]]:
        """
        convert list of list of floats into numpy array and preform predict
        :param features_list: list of list of floats
        :return: list of predictions and list of probabilities
        """
        if features_list is None:
            features_list = []
        X = []
        for features in features_list:
            keys = sorted(features.keys())
            values = [features[key] for key in keys]
            if F.is_list_of_list(values):
                values = F.flatten_list(values)
            X.append(values)
        if self.use_dummy_model:
            probabilities = [0] * len(features_list)
            predictions = [-1] * len(features_list)
        else:
            predictions, probabilities = self.do_predict(X)
        return predictions, probabilities

    def do_predict(self, encoded_features_np: np.ndarray) -> Tuple[List[float], List[float]]:
        """
        preform predictions
        :param encoded_features_np: numpy array
        :return: list of predictions and list of probabilities
        """
        raise NotImplementedError

    def post_predict(self, preds: List[float], probs: List[float], predictables: List[PredictableBase]) -> Tuple[
        List[float], List[float], List[PredictableBase]]:
        """
        insert prediction and probability into each candidate
        :param preds: list of prediction
        :param probs: list of probabilities
        :param predictables: the candidates
        :return: list of preds, list of probs and list of predictable objects
        """
        for idx, predictable in enumerate(predictables):
            predictable.set_prediction(preds[idx], probs[idx])
        return preds, probs, predictables
