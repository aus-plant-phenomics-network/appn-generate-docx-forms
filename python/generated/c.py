from .form_data_mixin import FormDataMixin
from .user_training_documentation import UserTrainingDocumentation

class C(FormDataMixin):
    _field_names = ['geneticallyModified_NLRD_C', 'geneticallyModified_NLRD_C_Id', 'geneticallyModified_NLRD_C_approval_letter', 'geneticallyModified_NLRD_C_IBC_approval_letter']
    _child_sections = ['user_training_documentation']

    def __init__(self, **kwargs):
        self._geneticallyModified_NLRD_C = None
        self.geneticallyModified_NLRD_C = kwargs.get('geneticallyModified_NLRD_C')
        self.geneticallyModified_NLRD_C_Id = kwargs.get('geneticallyModified_NLRD_C_Id')
        self.geneticallyModified_NLRD_C_approval_letter = kwargs.get('geneticallyModified_NLRD_C_approval_letter')
        self.geneticallyModified_NLRD_C_IBC_approval_letter = kwargs.get('geneticallyModified_NLRD_C_IBC_approval_letter')
        self.user_training_documentation = UserTrainingDocumentation()

    @property
    def geneticallyModified_NLRD_C(self):
        return self._geneticallyModified_NLRD_C

    @geneticallyModified_NLRD_C.setter
    def geneticallyModified_NLRD_C(self, value):
        if value is None:
            self._geneticallyModified_NLRD_C = None
            return
        allowed = ['C']
        if value not in allowed:
            raise ValueError(Invalid value for 'geneticallyModified_NLRD_C': {value}. Allowed values: {allowed}""")
        self._geneticallyModified_NLRD_C = value