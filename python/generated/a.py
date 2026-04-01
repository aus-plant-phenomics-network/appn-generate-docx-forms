from .form_data_mixin import FormDataMixin
from .b import B

class A(FormDataMixin):
    _field_names = ['geneticallyModified_NLRD_A', 'geneticallyModified_NLRD_A_Id', 'geneticallyModified_NLRD_A_approval_letter']
    _child_sections = ['b']

    def __init__(self, **kwargs):
        self._geneticallyModified_NLRD_A = None
        self.geneticallyModified_NLRD_A = kwargs.get('geneticallyModified_NLRD_A')
        self.geneticallyModified_NLRD_A_Id = kwargs.get('geneticallyModified_NLRD_A_Id')
        self.geneticallyModified_NLRD_A_approval_letter = kwargs.get('geneticallyModified_NLRD_A_approval_letter')
        self.b = B()

    @property
    def geneticallyModified_NLRD_A(self):
        return self._geneticallyModified_NLRD_A

    @geneticallyModified_NLRD_A.setter
    def geneticallyModified_NLRD_A(self, value):
        if value is None:
            self._geneticallyModified_NLRD_A = None
            return
        allowed = ['A']
        if value not in allowed:
            raise ValueError(Invalid value for 'geneticallyModified_NLRD_A': {value}. Allowed values: {allowed}""")
        self._geneticallyModified_NLRD_A = value