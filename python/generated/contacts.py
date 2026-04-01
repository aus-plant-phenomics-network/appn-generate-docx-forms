from .form_data_mixin import FormDataMixin
from .lab_leader_supervisor import LabLeaderSupervisor

class Contacts(FormDataMixin):
    _field_names = []
    _child_sections = ['lab_leader_supervisor']

    def __init__(self, **kwargs):
        self.lab_leader_supervisor = LabLeaderSupervisor()