#!/usr/bin/env python
# coding: utf-8
from typing import Any, Dict

from lib.shared.shared_objects import SharedArtifacts
from lib.base_classes.object_base import ObjectBase
from lib.config.zids_config import ZIDSConfig


class PredictableBase(ObjectBase):
    """
    Abstract class that store all instance data
    """

    def __init__(self, name: str, config: ZIDSConfig = None, shared_artifacts: SharedArtifacts = None, **kwargs):
        super(PredictableBase, self).__init__(name=name, config=config, shared_artifacts=shared_artifacts, **kwargs)
        self.reset_base()

    def reset_base(self) -> None:
        """
        assign all class members
        """
        self.reset_attributes()
        self.reset_prediction()
        self.reset_target()
        self.reset_forced()

    def reset_prediction(self) -> None:
        """
        reset the predictions
        """
        self.prediction = None
        self.prob = None

    def set_prediction(self, pred: Any, prob: float):
        """
        set the predictions
        :param pred: the prediction
        :param prob: the probability
        """
        self.prediction = pred
        self.prob = prob

    def set_target(self, target: Any) -> None:
        """
        set the target
        :param target: the target
        """
        self.target = target

    def reset_target(self) -> None:
        """
        rest the target
        """
        self.target = None

    def set_attributes(self, attributes: dict) -> None:
        """
        set attributes
        :param attributes:
        """
        self.attributes = attributes

    def get_attributes(self) -> Dict[str, Any]:
        """
        get the attributes
        :return: dict of attributes
        """
        return self.attributes

    def reset_attributes(self) -> None:
        """
        reset the attributes
        """
        self.attributes = {}

    def reset_forced(self) -> None:
        """
        reset the forced values
        """
        self.forced_predction = None
        self.forced_reason = ''

    def force_prediction(self, forced_predction: Any, forced_reason: str = '') -> None:
        """
        update the force prediction
        :param forced_predction: the force predciton
        :param forced_reason: the reason
        """
        self.forced_predction = forced_predction
        self.forced_reason = forced_reason

    def get_pred(self) -> Any:
        """
        return the prediction
        :return: the prediction (return forced prediction if it exist)
        """
        if self.forced_predction is not None:
            return self.forced_predction
        return self.prediction
