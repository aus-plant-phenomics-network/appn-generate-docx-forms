from .form_data_mixin import FormDataMixin
from .project_description import ProjectDescription

class AdelaideUniversityCustomers(FormDataMixin):
    _field_names = ['aucustomers_ProjectCode', 'aucustomers_BusUnit', 'aucustomers_Account', 'aucustomers_Fund', 'aucustomers_DeptID', 'aucustomers_Campus']
    _child_sections = ['project_description']

    def __init__(self, **kwargs):
        self.aucustomers_ProjectCode = kwargs.get('aucustomers_ProjectCode')
        self.aucustomers_BusUnit = kwargs.get('aucustomers_BusUnit')
        self.aucustomers_Account = kwargs.get('aucustomers_Account')
        self.aucustomers_Fund = kwargs.get('aucustomers_Fund')
        self.aucustomers_DeptID = kwargs.get('aucustomers_DeptID')
        self._aucustomers_Campus = None
        self.aucustomers_Campus = kwargs.get('aucustomers_Campus')
        self.project_description = ProjectDescription()

    @property
    def aucustomers_Campus(self):
        return self._aucustomers_Campus

    @aucustomers_Campus.setter
    def aucustomers_Campus(self, value):
        if value is None:
            self._aucustomers_Campus = None
            return
        allowed = ['Adelaide City Campus (North Terrace)', 'Magill Campus', 'Mawson Lakes Campus', 'Waite Campus', 'Roseworthy Campus', 'Mount Gambier Campus', 'Whyalla Campus']
        if value not in allowed:
            raise ValueError(Invalid value for 'aucustomers_Campus': {value}. Allowed values: {allowed}""")
        self._aucustomers_Campus = value