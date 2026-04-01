from .form_data_mixin import FormDataMixin
from .please_choose_your_between_a_b_or_c_as_described_below import PleaseChooseYourBetweenABOrCAsDescribedBelow

class PlantsSeedsGeneticModificationTerminologyOfficeOfTheGeneTechnologyRegulatorOgtrNotifiableLowRiskDealingsNlrd(FormDataMixin):
    _field_names = ['geneticallyModified_Modified']
    _child_sections = ['please_choose_your_between_a_b_or_c_as_described_below']

    def __init__(self, **kwargs):
        self._geneticallyModified_Modified = None
        self.geneticallyModified_Modified = kwargs.get('geneticallyModified_Modified')
        self.please_choose_your_between_a_b_or_c_as_described_below = PleaseChooseYourBetweenABOrCAsDescribedBelow()

    @property
    def geneticallyModified_Modified(self):
        return self._geneticallyModified_Modified

    @geneticallyModified_Modified.setter
    def geneticallyModified_Modified(self, value):
        if value is None:
            self._geneticallyModified_Modified = None
            return
        allowed = ['Yes', 'No']
        if value not in allowed:
            raise ValueError(Invalid value for 'geneticallyModified_Modified': {value}. Allowed values: {allowed}""")
        self._geneticallyModified_Modified = value