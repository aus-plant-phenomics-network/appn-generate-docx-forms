from .form_data_mixin import FormDataMixin
from .plants_seeds_genetic_modification_terminology_office_of_the_gene_technology_regulator_ogtr_notifiable_low_risk_dealings_nlrd import PlantsSeedsGeneticModificationTerminologyOfficeOfTheGeneTechnologyRegulatorOgtrNotifiableLowRiskDealingsNlrd

class FacilityAccess(FormDataMixin):
    _field_names = ['facilityAccess_keys', 'facilityAccess_desc', 'facilityAccess_person1Surname', 'facilityAccess_person1Firstname', 'facilityAccess_person1Email', 'facilityAccess_person1Phone', 'facilityAccess_person1Keys', 'facilityAccess_person2Surname', 'facilityAccess_person2Firstname', 'facilityAccess_person2Email', 'facilityAccess_person2Phone', 'facilityAccess_person2Keys', 'facilityAccess_person3Surname', 'facilityAccess_person3Firstname', 'facilityAccess_person3Email', 'facilityAccess_person3Phone', 'facilityAccess_person3Keys', 'facilityAccess_person4Surname', 'facilityAccess_person4Firstname', 'facilityAccess_person4Email', 'facilityAccess_person4Phone', 'facilityAccess_person4Keys', 'facilityAccess_otherRequirements']
    _child_sections = ['plants_seeds_genetic_modification_terminology_office_of_the_gene_technology_regulator_ogtr_notifiable_low_risk_dealings_nlrd']

    def __init__(self, **kwargs):
        self._facilityAccess_keys = None
        self.facilityAccess_keys = kwargs.get('facilityAccess_keys')
        self.facilityAccess_desc = kwargs.get('facilityAccess_desc')
        self.facilityAccess_person1Surname = kwargs.get('facilityAccess_person1Surname')
        self.facilityAccess_person1Firstname = kwargs.get('facilityAccess_person1Firstname')
        self.facilityAccess_person1Email = kwargs.get('facilityAccess_person1Email')
        self.facilityAccess_person1Phone = kwargs.get('facilityAccess_person1Phone')
        self._facilityAccess_person1Keys = None
        self.facilityAccess_person1Keys = kwargs.get('facilityAccess_person1Keys')
        self.facilityAccess_person2Surname = kwargs.get('facilityAccess_person2Surname')
        self.facilityAccess_person2Firstname = kwargs.get('facilityAccess_person2Firstname')
        self.facilityAccess_person2Email = kwargs.get('facilityAccess_person2Email')
        self.facilityAccess_person2Phone = kwargs.get('facilityAccess_person2Phone')
        self._facilityAccess_person2Keys = None
        self.facilityAccess_person2Keys = kwargs.get('facilityAccess_person2Keys')
        self.facilityAccess_person3Surname = kwargs.get('facilityAccess_person3Surname')
        self.facilityAccess_person3Firstname = kwargs.get('facilityAccess_person3Firstname')
        self.facilityAccess_person3Email = kwargs.get('facilityAccess_person3Email')
        self.facilityAccess_person3Phone = kwargs.get('facilityAccess_person3Phone')
        self._facilityAccess_person3Keys = None
        self.facilityAccess_person3Keys = kwargs.get('facilityAccess_person3Keys')
        self.facilityAccess_person4Surname = kwargs.get('facilityAccess_person4Surname')
        self.facilityAccess_person4Firstname = kwargs.get('facilityAccess_person4Firstname')
        self.facilityAccess_person4Email = kwargs.get('facilityAccess_person4Email')
        self.facilityAccess_person4Phone = kwargs.get('facilityAccess_person4Phone')
        self._facilityAccess_person4Keys = None
        self.facilityAccess_person4Keys = kwargs.get('facilityAccess_person4Keys')
        self.facilityAccess_otherRequirements = kwargs.get('facilityAccess_otherRequirements')
        self.plants_seeds_genetic_modification_terminology_office_of_the_gene_technology_regulator_ogtr_notifiable_low_risk_dealings_nlrd = PlantsSeedsGeneticModificationTerminologyOfficeOfTheGeneTechnologyRegulatorOgtrNotifiableLowRiskDealingsNlrd()

    @property
    def facilityAccess_keys(self):
        return self._facilityAccess_keys

    @facilityAccess_keys.setter
    def facilityAccess_keys(self, value):
        if value is None:
            self._facilityAccess_keys = None
            return
        allowed = ['Check if required']
        if value not in allowed:
            raise ValueError(Invalid value for 'facilityAccess_keys': {value}. Allowed values: {allowed}""")
        self._facilityAccess_keys = value

    @property
    def facilityAccess_person1Keys(self):
        return self._facilityAccess_person1Keys

    @facilityAccess_person1Keys.setter
    def facilityAccess_person1Keys(self, value):
        if value is None:
            self._facilityAccess_person1Keys = None
            return
        allowed = ['Check if required']
        if value not in allowed:
            raise ValueError(Invalid value for 'facilityAccess_person1Keys': {value}. Allowed values: {allowed}""")
        self._facilityAccess_person1Keys = value

    @property
    def facilityAccess_person2Keys(self):
        return self._facilityAccess_person2Keys

    @facilityAccess_person2Keys.setter
    def facilityAccess_person2Keys(self, value):
        if value is None:
            self._facilityAccess_person2Keys = None
            return
        allowed = ['Check if required']
        if value not in allowed:
            raise ValueError(Invalid value for 'facilityAccess_person2Keys': {value}. Allowed values: {allowed}""")
        self._facilityAccess_person2Keys = value

    @property
    def facilityAccess_person3Keys(self):
        return self._facilityAccess_person3Keys

    @facilityAccess_person3Keys.setter
    def facilityAccess_person3Keys(self, value):
        if value is None:
            self._facilityAccess_person3Keys = None
            return
        allowed = ['Check if required']
        if value not in allowed:
            raise ValueError(Invalid value for 'facilityAccess_person3Keys': {value}. Allowed values: {allowed}""")
        self._facilityAccess_person3Keys = value

    @property
    def facilityAccess_person4Keys(self):
        return self._facilityAccess_person4Keys

    @facilityAccess_person4Keys.setter
    def facilityAccess_person4Keys(self, value):
        if value is None:
            self._facilityAccess_person4Keys = None
            return
        allowed = ['Check if required']
        if value not in allowed:
            raise ValueError(Invalid value for 'facilityAccess_person4Keys': {value}. Allowed values: {allowed}""")
        self._facilityAccess_person4Keys = value