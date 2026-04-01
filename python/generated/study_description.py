from .form_data_mixin import FormDataMixin
from .contacts import Contacts

class StudyDescription(FormDataMixin):
    _field_names = ['appn:ResearchActivity:code', 'appn:Study', 'studyDescription']
    _child_sections = ['contacts']

    def __init__(self, **kwargs):
        self.appn:ResearchActivity:code = kwargs.get('appn:ResearchActivity:code')
        self.appn:Study = kwargs.get('appn:Study')
        self.studyDescription = kwargs.get('studyDescription')
        self.contacts = Contacts()