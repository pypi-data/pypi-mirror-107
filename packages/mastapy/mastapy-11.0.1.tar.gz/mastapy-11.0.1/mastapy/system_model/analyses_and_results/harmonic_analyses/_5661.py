'''_5661.py

FaceGearHarmonicAnalysis
'''


from mastapy.system_model.part_model.gears import _2204
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6529
from mastapy.system_model.analyses_and_results.system_deflections import _2423
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5667
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FaceGearHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearHarmonicAnalysis',)


class FaceGearHarmonicAnalysis(_5667.GearHarmonicAnalysis):
    '''FaceGearHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2204.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2204.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6529.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6529.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2423.FaceGearSystemDeflection':
        '''FaceGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2423.FaceGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
