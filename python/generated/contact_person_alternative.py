from .form_data_mixin import FormDataMixin
from .source_of_funding import SourceOfFunding

class ContactPersonAlternative(FormDataMixin):
    _field_names = ['contactPerson2_firstname', 'contactPerson2_lastname', 'contactPerson2_orcid', 'contactPerson2_email', 'contactPerson2_phone', 'contactPerson2_mobile', 'contactPerson2_fax', 'contactPerson2_institution', 'contactPerson2_instStreetAddress']
    _child_sections = ['source_of_funding']

    def __init__(self, **kwargs):
        self.contactPerson2_firstname = kwargs.get('contactPerson2_firstname')
        self.contactPerson2_lastname = kwargs.get('contactPerson2_lastname')
        self.contactPerson2_orcid = kwargs.get('contactPerson2_orcid')
        self.contactPerson2_email = kwargs.get('contactPerson2_email')
        self.contactPerson2_phone = kwargs.get('contactPerson2_phone')
        self.contactPerson2_mobile = kwargs.get('contactPerson2_mobile')
        self.contactPerson2_fax = kwargs.get('contactPerson2_fax')
        self._contactPerson2_institution = None
        self.contactPerson2_institution = kwargs.get('contactPerson2_institution')
        self.contactPerson2_instStreetAddress = kwargs.get('contactPerson2_instStreetAddress')
        self.source_of_funding = SourceOfFunding()

    @property
    def contactPerson2_institution(self):
        return self._contactPerson2_institution

    @contactPerson2_institution.setter
    def contactPerson2_institution(self, value):
        if value is None:
            self._contactPerson2_institution = None
            return
        allowed = ['empty', 'Adelaide University (https://ror.org/00892tw58)', 'Australian Catholic University (https://ror.org/02bfwt286)', 'Australian National University (https://ror.org/019wvm592)', 'Bond University (https://ror.org/03y7k4s08)', 'Central Queensland University (https://ror.org/00jbnf214)', 'Charles Darwin University (https://ror.org/02j9q8k02)', 'Charles Sturt University (https://ror.org/03gxk6z40)', 'Curtin University (https://ror.org/02n415q13)', 'Deakin University (https://ror.org/00g5s8h70)', 'Edith Cowan University (https://ror.org/01p5r2w48)', 'Federation University Australia (https://ror.org/04ttjf776)', 'Flinders University (https://ror.org/03m2x1q45)', 'Griffith University (https://ror.org/02q5xgk87)', 'James Cook University (https://ror.org/01n6g0j11)', 'La Trobe University (https://ror.org/04t3k5w24)', 'Macquarie University (https://ror.org/02bfwt286)', 'Monash University (https://ror.org/02bfwt286)', 'Murdoch University (https://ror.org/03y7k4s08)', 'Queensland University of Technology (https://ror.org/01v9k7x03)', 'RMIT University (https://ror.org/04ttjf776)', 'Southern Cross University (https://ror.org/03p1k5r68)', 'Swinburne University of Technology (https://ror.org/03taz7m60)', 'Torrens University Australia (https://ror.org/01y2j7h59)', 'University of Adelaide (https://ror.org/01y2j7h59)', 'University of Canberra (https://ror.org/04s1gkz69)', 'University of Melbourne (https://ror.org/03yrm5c26)', 'University of New England (Australia) (https://ror.org/02k8vdy47)', 'University of New South Wales (https://ror.org/03r8z3t63)', 'University of Newcastle (Australia) (https://ror.org/01sf06y89)', 'University of Queensland (https://ror.org/03xtv2k96)', 'University of South Australia (https://ror.org/01n9nmr07)', 'University of Southern Queensland (https://ror.org/01q9g0j48)', 'University of Sydney (https://ror.org/0384j8v12)', 'University of Tasmania (https://ror.org/04d7h8x64)', 'University of Technology Sydney (https://ror.org/03f0f6041)', 'University of the Sunshine Coast (https://ror.org/04g1s3d33)', 'University of Western Australia (https://ror.org/01jz6c177)', 'University of Wollongong (https://ror.org/00hj54h04)', 'Victoria University (https://ror.org/00hx57361)', 'Western Sydney University (https://ror.org/03qjg6k89)', 'Department of Agriculture, Fisheries and Forestry (Australia) (https://ror.org/01na82s61)', 'NSW Department of Primary Industries (https://ror.org/01awp2978)', 'Commonwealth Scientific and Industrial Research Organisation (CSIRO) (https://ror.org/03qn8fb07)', 'Australian Centre for International Agricultural Research (https://ror.org/035y5td47)']
        if value not in allowed:
            raise ValueError(Invalid value for 'contactPerson2_institution': {value}. Allowed values: {allowed}""")
        self._contactPerson2_institution = value