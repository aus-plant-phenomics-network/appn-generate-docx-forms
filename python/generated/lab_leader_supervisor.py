from .form_data_mixin import FormDataMixin
from .contact_person_alternative import ContactPersonAlternative

class LabLeaderSupervisor(FormDataMixin):
    _field_names = ['contactPerson1_firstname', 'contactPerson1_lastname', 'contactPerson1_orcid', 'contactPerson1_email', 'contactPerson1_phone', 'contactPerson1_mobile', 'contactPerson1_fax', 'contactPerson1_postaladdress', 'contactPerson1_physicaladdress', 'contactPerson1_institution', 'contactPerson1_institutionother', 'contactPerson1_ABN', 'contactPerson1_instStreetAddress']
    _child_sections = ['contact_person_alternative']

    def __init__(self, **kwargs):
        self.contactPerson1_firstname = kwargs.get('contactPerson1_firstname')
        self.contactPerson1_lastname = kwargs.get('contactPerson1_lastname')
        self.contactPerson1_orcid = kwargs.get('contactPerson1_orcid')
        self.contactPerson1_email = kwargs.get('contactPerson1_email')
        self.contactPerson1_phone = kwargs.get('contactPerson1_phone')
        self.contactPerson1_mobile = kwargs.get('contactPerson1_mobile')
        self.contactPerson1_fax = kwargs.get('contactPerson1_fax')
        self.contactPerson1_postaladdress = kwargs.get('contactPerson1_postaladdress')
        self.contactPerson1_physicaladdress = kwargs.get('contactPerson1_physicaladdress')
        self._contactPerson1_institution = None
        self.contactPerson1_institution = kwargs.get('contactPerson1_institution')
        self.contactPerson1_institutionother = kwargs.get('contactPerson1_institutionother')
        self.contactPerson1_ABN = kwargs.get('contactPerson1_ABN')
        self.contactPerson1_instStreetAddress = kwargs.get('contactPerson1_instStreetAddress')
        self.contact_person_alternative = ContactPersonAlternative()

    @property
    def contactPerson1_institution(self):
        return self._contactPerson1_institution

    @contactPerson1_institution.setter
    def contactPerson1_institution(self, value):
        if value is None:
            self._contactPerson1_institution = None
            return
        allowed = ['empty', 'Adelaide University (https://ror.org/00892tw58)', 'Australian Catholic University (https://ror.org/02bfwt286)', 'Australian National University (https://ror.org/019wvm592)', 'Bond University (https://ror.org/03y7k4s08)', 'Central Queensland University (https://ror.org/00jbnf214)', 'Charles Darwin University (https://ror.org/02j9q8k02)', 'Charles Sturt University (https://ror.org/03gxk6z40)', 'Curtin University (https://ror.org/02n415q13)', 'Deakin University (https://ror.org/00g5s8h70)', 'Edith Cowan University (https://ror.org/01p5r2w48)', 'Federation University Australia (https://ror.org/04ttjf776)', 'Flinders University (https://ror.org/03m2x1q45)', 'Griffith University (https://ror.org/02q5xgk87)', 'James Cook University (https://ror.org/01n6g0j11)', 'La Trobe University (https://ror.org/04t3k5w24)', 'Macquarie University (https://ror.org/02bfwt286)', 'Monash University (https://ror.org/02bfwt286)', 'Murdoch University (https://ror.org/03y7k4s08)', 'Queensland University of Technology (https://ror.org/01v9k7x03)', 'RMIT University (https://ror.org/04ttjf776)', 'Southern Cross University (https://ror.org/03p1k5r68)', 'Swinburne University of Technology (https://ror.org/03taz7m60)', 'Torrens University Australia (https://ror.org/01y2j7h59)', 'University of Adelaide (https://ror.org/01y2j7h59)', 'University of Canberra (https://ror.org/04s1gkz69)', 'University of Melbourne (https://ror.org/03yrm5c26)', 'University of New England (Australia) (https://ror.org/02k8vdy47)', 'University of New South Wales (https://ror.org/03r8z3t63)', 'University of Newcastle (Australia) (https://ror.org/01sf06y89)', 'University of Queensland (https://ror.org/03xtv2k96)', 'University of South Australia (https://ror.org/01n9nmr07)', 'University of Southern Queensland (https://ror.org/01q9g0j48)', 'University of Sydney (https://ror.org/0384j8v12)', 'University of Tasmania (https://ror.org/04d7h8x64)', 'University of Technology Sydney (https://ror.org/03f0f6041)', 'University of the Sunshine Coast (https://ror.org/04g1s3d33)', 'University of Western Australia (https://ror.org/01jz6c177)', 'University of Wollongong (https://ror.org/00hj54h04)', 'Victoria University (https://ror.org/00hx57361)', 'Western Sydney University (https://ror.org/03qjg6k89)', 'Department of Agriculture, Fisheries and Forestry (Australia) (https://ror.org/01na82s61)', 'NSW Department of Primary Industries (https://ror.org/01awp2978)', 'Commonwealth Scientific and Industrial Research Organisation (CSIRO) (https://ror.org/03qn8fb07)', 'Australian Centre for International Agricultural Research (https://ror.org/035y5td47)']
        if value not in allowed:
            raise ValueError(Invalid value for 'contactPerson1_institution': {value}. Allowed values: {allowed}""")
        self._contactPerson1_institution = value