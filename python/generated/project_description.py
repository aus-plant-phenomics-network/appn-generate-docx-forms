from .form_data_mixin import FormDataMixin
from .xray_ct_hire import XrayCtHire

class ProjectDescription(FormDataMixin):
    _field_names = ['project_Description']
    _child_sections = ['xray_ct_hire']

    def __init__(self, **kwargs):
        self.project_Description = kwargs.get('project_Description')
        self.xray_ct_hire = XrayCtHire()