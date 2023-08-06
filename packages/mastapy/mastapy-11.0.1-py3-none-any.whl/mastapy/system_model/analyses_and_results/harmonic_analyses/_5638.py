'''_5638.py

CVTPulleyHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2263
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2402
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5708
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CVTPulleyHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyHarmonicAnalysis',)


class CVTPulleyHarmonicAnalysis(_5708.PulleyHarmonicAnalysis):
    '''CVTPulleyHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2263.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2263.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2402.CVTPulleySystemDeflection':
        '''CVTPulleySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2402.CVTPulleySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
