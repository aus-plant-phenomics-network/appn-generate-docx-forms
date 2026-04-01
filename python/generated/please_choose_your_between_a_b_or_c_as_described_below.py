from .form_data_mixin import FormDataMixin
from .a import A

class PleaseChooseYourBetweenABOrCAsDescribedBelow(FormDataMixin):
    _field_names = []
    _child_sections = ['a']

    def __init__(self, **kwargs):
        self.a = A()