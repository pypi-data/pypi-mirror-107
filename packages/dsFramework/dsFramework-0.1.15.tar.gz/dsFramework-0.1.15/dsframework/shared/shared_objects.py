"""
Object that store objects that are shared between all pipeline
"""


class SharedArtifacts:
    """
    Object that store objects that are shared between all pipeline
    """

    def __init__(self):
        self.object_dict = dict()

    def save_object(self, name: str, obj):
        """
        save object of
        :param name: the name of object
        :param obj: the object
        """
        self.object_dict[name] = obj

    def get_object(self, name: str, copy=False):
        """
        return object that stored
        :param name: the name of object
        :param copy: return shallow copy or not (using copy function)
        :return: a object
        """
        if name in self.object_dict:
            if copy:
                return self.object_dict[name].copy()
            else:
                return self.object_dict[name]
        else:
            return None
