from .form_data_mixin import FormDataMixin
from .c import C

class B(FormDataMixin):
    _field_names = ['geneticallyModified_NLRD_B', 'geneticallyModified_NLRD_B_Id', 'geneticallyModified_NLRD_B_approval_letter', 'geneticallyModified_NLRD_B_IBC_approval_letter']
    _child_sections = ['c']

    def __init__(self, **kwargs):
        self._geneticallyModified_NLRD_B = None
        self.geneticallyModified_NLRD_B = kwargs.get('geneticallyModified_NLRD_B')
        self.geneticallyModified_NLRD_B_Id = kwargs.get('geneticallyModified_NLRD_B_Id')
        self.geneticallyModified_NLRD_B_approval_letter = kwargs.get('geneticallyModified_NLRD_B_approval_letter')
        self.geneticallyModified_NLRD_B_IBC_approval_letter = kwargs.get('geneticallyModified_NLRD_B_IBC_approval_letter')
        self.c = C()

    @property
    def geneticallyModified_NLRD_B(self):
        return self._geneticallyModified_NLRD_B

    @geneticallyModified_NLRD_B.setter
    def geneticallyModified_NLRD_B(self, value):
        if value is None:
            self._geneticallyModified_NLRD_B = None
            return
        allowed = ['B']
        if value not in allowed:
            raise ValueError(Invalid value for 'geneticallyModified_NLRD_B': {value}. Allowed values: {allowed}""")
        self._geneticallyModified_NLRD_B = value