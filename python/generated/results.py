from .form_data_mixin import FormDataMixin
from .facility_access import FacilityAccess

class Results(FormDataMixin):
    _field_names = ['results_AnalysisNote', 'results_AnalysisTraitsGrainSpike', 'results_AnalysisAdditionalNote', 'results_AnalysisTraitsExtra', 'results_AnalysisTraitsExtraNoteContact', 'results_AnalysisTraitsExtraNote', 'results_AnalysisTraitsOGTRtraining']
    _child_sections = ['facility_access']

    def __init__(self, **kwargs):
        self.results_AnalysisNote = kwargs.get('results_AnalysisNote')
        self._results_AnalysisTraitsGrainSpike = None
        self.results_AnalysisTraitsGrainSpike = kwargs.get('results_AnalysisTraitsGrainSpike')
        self.results_AnalysisAdditionalNote = kwargs.get('results_AnalysisAdditionalNote')
        self._results_AnalysisTraitsExtra = None
        self.results_AnalysisTraitsExtra = kwargs.get('results_AnalysisTraitsExtra')
        self.results_AnalysisTraitsExtraNoteContact = kwargs.get('results_AnalysisTraitsExtraNoteContact')
        self.results_AnalysisTraitsExtraNote = kwargs.get('results_AnalysisTraitsExtraNote')
        self._results_AnalysisTraitsOGTRtraining = None
        self.results_AnalysisTraitsOGTRtraining = kwargs.get('results_AnalysisTraitsOGTRtraining')
        self.facility_access = FacilityAccess()

    @property
    def results_AnalysisTraitsGrainSpike(self):
        return self._results_AnalysisTraitsGrainSpike

    @results_AnalysisTraitsGrainSpike.setter
    def results_AnalysisTraitsGrainSpike(self, value):
        if value is None:
            self._results_AnalysisTraitsGrainSpike = None
            return
        allowed = ['Grain traits: grain number, weight, morphology (volume, surface area, length)', 'Spike traits: spike length, spike dimension (please specify). ']
        if value not in allowed:
            raise ValueError(Invalid value for 'results_AnalysisTraitsGrainSpike': {value}. Allowed values: {allowed}""")
        self._results_AnalysisTraitsGrainSpike = value

    @property
    def results_AnalysisTraitsExtra(self):
        return self._results_AnalysisTraitsExtra

    @results_AnalysisTraitsExtra.setter
    def results_AnalysisTraitsExtra(self, value):
        if value is None:
            self._results_AnalysisTraitsExtra = None
            return
        allowed = ['Spike 3D structure ', 'Spikelet analysis', 'Peduncle/stem analysis', 'Special reqirement (add below)', 'Video and imaging']
        if value not in allowed:
            raise ValueError(Invalid value for 'results_AnalysisTraitsExtra': {value}. Allowed values: {allowed}""")
        self._results_AnalysisTraitsExtra = value

    @property
    def results_AnalysisTraitsOGTRtraining(self):
        return self._results_AnalysisTraitsOGTRtraining

    @results_AnalysisTraitsOGTRtraining.setter
    def results_AnalysisTraitsOGTRtraining(self, value):
        if value is None:
            self._results_AnalysisTraitsOGTRtraining = None
            return
        allowed = ['Check if provided']
        if value not in allowed:
            raise ValueError(Invalid value for 'results_AnalysisTraitsOGTRtraining': {value}. Allowed values: {allowed}""")
        self._results_AnalysisTraitsOGTRtraining = value