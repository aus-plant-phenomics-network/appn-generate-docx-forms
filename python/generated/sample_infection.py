from .form_data_mixin import FormDataMixin
from .imported_seeds_quarantine_material import ImportedSeedsQuarantineMaterial

class SampleInfection(FormDataMixin):
    _field_names = ['infections_YesNo', 'infected_YesNo', 'infected_GM_YesNo', 'infections_Description']
    _child_sections = ['imported_seeds_quarantine_material']

    def __init__(self, **kwargs):
        self._infections_YesNo = None
        self.infections_YesNo = kwargs.get('infections_YesNo')
        self.infected_YesNo = kwargs.get('infected_YesNo')
        self._infected_GM_YesNo = None
        self.infected_GM_YesNo = kwargs.get('infected_GM_YesNo')
        self.infections_Description = kwargs.get('infections_Description')
        self.imported_seeds_quarantine_material = ImportedSeedsQuarantineMaterial()

    @property
    def infections_YesNo(self):
        return self._infections_YesNo

    @infections_YesNo.setter
    def infections_YesNo(self, value):
        if value is None:
            self._infections_YesNo = None
            return
        allowed = ['Yes', 'No']
        if value not in allowed:
            raise ValueError(Invalid value for 'infections_YesNo': {value}. Allowed values: {allowed}""")
        self._infections_YesNo = value

    @property
    def infected_GM_YesNo(self):
        return self._infected_GM_YesNo

    @infected_GM_YesNo.setter
    def infected_GM_YesNo(self, value):
        if value is None:
            self._infected_GM_YesNo = None
            return
        allowed = ['Yes', 'No']
        if value not in allowed:
            raise ValueError(Invalid value for 'infected_GM_YesNo': {value}. Allowed values: {allowed}""")
        self._infected_GM_YesNo = value