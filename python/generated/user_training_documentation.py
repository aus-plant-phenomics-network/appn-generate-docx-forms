from .form_data_mixin import FormDataMixin
from .sample_infection import SampleInfection

class UserTrainingDocumentation(FormDataMixin):
    _field_names = ['geneticallyModified_OGTR_training', 'geneticallyModified_OGTR_trainingDoc']
    _child_sections = ['sample_infection']

    def __init__(self, **kwargs):
        self._geneticallyModified_OGTR_training = None
        self.geneticallyModified_OGTR_training = kwargs.get('geneticallyModified_OGTR_training')
        self.geneticallyModified_OGTR_trainingDoc = kwargs.get('geneticallyModified_OGTR_trainingDoc')
        self.sample_infection = SampleInfection()

    @property
    def geneticallyModified_OGTR_training(self):
        return self._geneticallyModified_OGTR_training

    @geneticallyModified_OGTR_training.setter
    def geneticallyModified_OGTR_training(self, value):
        if value is None:
            self._geneticallyModified_OGTR_training = None
            return
        allowed = ['OGTR user training documentation attached']
        if value not in allowed:
            raise ValueError(Invalid value for 'geneticallyModified_OGTR_training': {value}. Allowed values: {allowed}""")
        self._geneticallyModified_OGTR_training = value