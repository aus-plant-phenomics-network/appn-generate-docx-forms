from .form_data_mixin import FormDataMixin
from .results import Results

class SampleInformation(FormDataMixin):
    _field_names = ['plants_or_crop', 'plants_or_crop_Name', 'plants_or_crop_NameOther', 'plants_or_crop_GM', 'plants_or_crop_GMExtraInfo', 'plants_or_crop_NumberOfHeads', 'plants_or_crop_SamplesOrdered', 'plants_or_crop_SamplesReturned', 'plants_or_crop_SamplesReturnedShipping', 'plants_or_crop_SamplesReminder', 'plants_or_crop_SamplesSpreadsheet', 'plants_or_crop_SamplesOtherInfo', 'plants_or_crop_SamplesTrialDesign_cb', 'plants_or_crop_SamplesTrialDesignTPA_cb', 'plants_or_crop_SamplesTrialDesignOther_rt', 'traits_Required']
    _child_sections = ['results']

    def __init__(self, **kwargs):
        self.plants_or_crop = kwargs.get('plants_or_crop')
        self._plants_or_crop_Name = None
        self.plants_or_crop_Name = kwargs.get('plants_or_crop_Name')
        self.plants_or_crop_NameOther = kwargs.get('plants_or_crop_NameOther')
        self._plants_or_crop_GM = None
        self.plants_or_crop_GM = kwargs.get('plants_or_crop_GM')
        self.plants_or_crop_GMExtraInfo = kwargs.get('plants_or_crop_GMExtraInfo')
        self.plants_or_crop_NumberOfHeads = kwargs.get('plants_or_crop_NumberOfHeads')
        self._plants_or_crop_SamplesOrdered = None
        self.plants_or_crop_SamplesOrdered = kwargs.get('plants_or_crop_SamplesOrdered')
        self._plants_or_crop_SamplesReturned = None
        self.plants_or_crop_SamplesReturned = kwargs.get('plants_or_crop_SamplesReturned')
        self.plants_or_crop_SamplesReturnedShipping = kwargs.get('plants_or_crop_SamplesReturnedShipping')
        self.plants_or_crop_SamplesReminder = kwargs.get('plants_or_crop_SamplesReminder')
        self.plants_or_crop_SamplesSpreadsheet = kwargs.get('plants_or_crop_SamplesSpreadsheet')
        self.plants_or_crop_SamplesOtherInfo = kwargs.get('plants_or_crop_SamplesOtherInfo')
        self._plants_or_crop_SamplesTrialDesign_cb = None
        self.plants_or_crop_SamplesTrialDesign_cb = kwargs.get('plants_or_crop_SamplesTrialDesign_cb')
        self._plants_or_crop_SamplesTrialDesignTPA_cb = None
        self.plants_or_crop_SamplesTrialDesignTPA_cb = kwargs.get('plants_or_crop_SamplesTrialDesignTPA_cb')
        self.plants_or_crop_SamplesTrialDesignOther_rt = kwargs.get('plants_or_crop_SamplesTrialDesignOther_rt')
        self._traits_Required = None
        self.traits_Required = kwargs.get('traits_Required')
        self.results = Results()

    @property
    def plants_or_crop_Name(self):
        return self._plants_or_crop_Name

    @plants_or_crop_Name.setter
    def plants_or_crop_Name(self, value):
        if value is None:
            self._plants_or_crop_Name = None
            return
        allowed = ['Triticum aestivum (wheat)', 'Oryza sativa (rice)', 'Zea mays (maize / corn)', 'Hordeum vulgare (barley)', 'Avena sativa (oats)', 'Sorghum bicolor (sorghum)', 'Pennisetum glaucum (pearl millet)', 'Glycine max (soybean)', 'Phaseolus vulgaris (common bean)', 'Pisum sativum (pea)', 'Cicer arietinum (chickpea)', 'Lens culinaris (lentil)', 'Arachis hypogaea (peanut / groundnut)', 'Solanum tuberosum (potato)', 'Manihot esculenta (cassava)', 'Ipomoea batatas (sweet potato)', 'Dioscorea alata (yam)', 'Beta vulgaris (sugar beet)', 'Brassica napus (canola / rapeseed)', 'Helianthus annuus (sunflower)', 'Elaeis guineensis (oil palm)', 'Cocos nucifera (coconut)', 'Sesamum indicum (sesame)', 'Gossypium hirsutum (cotton)', 'Linum usitatissimum (flax)', 'Corchorus olitorius (jute)', 'Malus domestica (apple)', 'Musa × paradisiaca (banana / plantain)', 'Citrus sinensis (sweet orange)', 'Vitis vinifera (grape)', 'Mangifera indica (mango)', 'Solanum lycopersicum (tomato)', 'Capsicum annuum (pepper)', 'Allium cepa (onion)', 'Brassica oleracea (cabbage)', 'Cucumis sativus (cucumber)']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_Name': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_Name = value

    @property
    def plants_or_crop_GM(self):
        return self._plants_or_crop_GM

    @plants_or_crop_GM.setter
    def plants_or_crop_GM(self, value):
        if value is None:
            self._plants_or_crop_GM = None
            return
        allowed = ['No', 'Yes']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_GM': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_GM = value

    @property
    def plants_or_crop_SamplesOrdered(self):
        return self._plants_or_crop_SamplesOrdered

    @plants_or_crop_SamplesOrdered.setter
    def plants_or_crop_SamplesOrdered(self, value):
        if value is None:
            self._plants_or_crop_SamplesOrdered = None
            return
        allowed = ['No', 'Yes']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_SamplesOrdered': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_SamplesOrdered = value

    @property
    def plants_or_crop_SamplesReturned(self):
        return self._plants_or_crop_SamplesReturned

    @plants_or_crop_SamplesReturned.setter
    def plants_or_crop_SamplesReturned(self, value):
        if value is None:
            self._plants_or_crop_SamplesReturned = None
            return
        allowed = ['No', 'Yes']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_SamplesReturned': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_SamplesReturned = value

    @property
    def plants_or_crop_SamplesTrialDesign_cb(self):
        return self._plants_or_crop_SamplesTrialDesign_cb

    @plants_or_crop_SamplesTrialDesign_cb.setter
    def plants_or_crop_SamplesTrialDesign_cb(self, value):
        if value is None:
            self._plants_or_crop_SamplesTrialDesign_cb = None
            return
        allowed = ['Plots are designed']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_SamplesTrialDesign_cb': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_SamplesTrialDesign_cb = value

    @property
    def plants_or_crop_SamplesTrialDesignTPA_cb(self):
        return self._plants_or_crop_SamplesTrialDesignTPA_cb

    @plants_or_crop_SamplesTrialDesignTPA_cb.setter
    def plants_or_crop_SamplesTrialDesignTPA_cb(self, value):
        if value is None:
            self._plants_or_crop_SamplesTrialDesignTPA_cb = None
            return
        allowed = ['Designed by TPA']
        if value not in allowed:
            raise ValueError(Invalid value for 'plants_or_crop_SamplesTrialDesignTPA_cb': {value}. Allowed values: {allowed}""")
        self._plants_or_crop_SamplesTrialDesignTPA_cb = value

    @property
    def traits_Required(self):
        return self._traits_Required

    @traits_Required.setter
    def traits_Required(self, value):
        if value is None:
            self._traits_Required = None
            return
        allowed = ['Cross if understood']
        if value not in allowed:
            raise ValueError(Invalid value for 'traits_Required': {value}. Allowed values: {allowed}""")
        self._traits_Required = value