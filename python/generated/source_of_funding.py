from .form_data_mixin import FormDataMixin
from .adelaide_university_customers import AdelaideUniversityCustomers

class SourceOfFunding(FormDataMixin):
    _field_names = ['funding_Source', 'funding_Research_pc', 'funding_Commercial_pc', 'funding_GrantDescription', 'funding_Collaborators']
    _child_sections = ['adelaide_university_customers']

    def __init__(self, **kwargs):
        self.funding_Source = kwargs.get('funding_Source')
        self.funding_Research_pc = kwargs.get('funding_Research_pc')
        self.funding_Commercial_pc = kwargs.get('funding_Commercial_pc')
        self.funding_GrantDescription = kwargs.get('funding_GrantDescription')
        self.funding_Collaborators = kwargs.get('funding_Collaborators')
        self.adelaide_university_customers = AdelaideUniversityCustomers()