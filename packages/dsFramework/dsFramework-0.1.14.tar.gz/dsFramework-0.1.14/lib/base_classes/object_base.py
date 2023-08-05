"""
Object that is based for all objects in the framework
"""
from lib.shared.shared_objects import SharedArtifacts
from lib.config.zids_config import ZIDSConfig
from lib.utils import functions


class ObjectBase:
    """
    Object that is based for all objects in the framework
    """

    def __init__(self, shared_artifacts: SharedArtifacts, config: ZIDSConfig, name: str = "object_base", **kwargs):
        """
        :param name: the name of object (for logger issues)
        :param shared_artifacts: a objects that are shared between the all the pipeline
        :param config: configuration of the object
        :param str: the name of class (that will print in logger)
        :param kwargs: extra parameters of custom use
        """
        self.name = name
        self.shared_objects = shared_artifacts
        self.config = config
        self.F = functions

    def set_config(self, config: ZIDSConfig) -> None:
        """
        set config object
        :param config: the config object
        """
        self.config = config

    def set_shared_objects(self, shared_objects: SharedArtifacts) -> None:
        """
        set SharedObjects member
        :param shared_objects: the shared objects
        """
        self.shared_objects = shared_objects

