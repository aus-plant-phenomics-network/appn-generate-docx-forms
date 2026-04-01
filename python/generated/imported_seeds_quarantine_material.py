from .form_data_mixin import FormDataMixin
from .quality_assurance_framework_qap_accredited_persons_responsible_for_this_project_are import QualityAssuranceFrameworkQapAccreditedPersonsResponsibleForThisProjectAre

class ImportedSeedsQuarantineMaterial(FormDataMixin):
    _field_names = ['quarantine_YesNo', 'quarantine_ImportPermitNo', 'quarantine_ExpiryDate', 'quarantine_YesNo']
    _child_sections = ['quality_assurance_framework_qap_accredited_persons_responsible_for_this_project_are']

    def __init__(self, **kwargs):
        self._quarantine_YesNo = None
        self.quarantine_YesNo = kwargs.get('quarantine_YesNo')
        self.quarantine_ImportPermitNo = kwargs.get('quarantine_ImportPermitNo')
        self.quarantine_ExpiryDate = kwargs.get('quarantine_ExpiryDate')
        self._quarantine_YesNo = None
        self.quarantine_YesNo = kwargs.get('quarantine_YesNo')
        self.quality_assurance_framework_qap_accredited_persons_responsible_for_this_project_are = QualityAssuranceFrameworkQapAccreditedPersonsResponsibleForThisProjectAre()

    @property
    def quarantine_YesNo(self):
        return self._quarantine_YesNo

    @quarantine_YesNo.setter
    def quarantine_YesNo(self, value):
        if value is None:
            self._quarantine_YesNo = None
            return
        allowed = ['Yes', 'No']
        if value not in allowed:
            raise ValueError(Invalid value for 'quarantine_YesNo': {value}. Allowed values: {allowed}""")
        self._quarantine_YesNo = value

    @property
    def quarantine_YesNo(self):
        return self._quarantine_YesNo

    @quarantine_YesNo.setter
    def quarantine_YesNo(self, value):
        if value is None:
            self._quarantine_YesNo = None
            return
        allowed = ['Yes', 'No']
        if value not in allowed:
            raise ValueError(Invalid value for 'quarantine_YesNo': {value}. Allowed values: {allowed}""")
        self._quarantine_YesNo = value