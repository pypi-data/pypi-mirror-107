

from dsframework.testable.sample import DatasetSample


class ExtendedDatasetSample(DatasetSample):
    def __init__(self, name='dataset_sample', x=None, y=None, features=None, pred=-1, pre_forcer_pred=None, prob=-1):
        super().__init__(name=name, x=x, y=y, features=features, pred=pred, prob=prob)
        self.pre_forcer_pred = pre_forcer_pred

