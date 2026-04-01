from .form_data_mixin import FormDataMixin
from .sample_information import SampleInformation

class XrayCtHire(FormDataMixin):
    _field_names = ['xrayHire_StartDate', 'xrayHire_EndDate']
    _child_sections = ['sample_information']

    def __init__(self, **kwargs):
        self.xrayHire_StartDate = kwargs.get('xrayHire_StartDate')
        self.xrayHire_EndDate = kwargs.get('xrayHire_EndDate')
        self.sample_information = SampleInformation()