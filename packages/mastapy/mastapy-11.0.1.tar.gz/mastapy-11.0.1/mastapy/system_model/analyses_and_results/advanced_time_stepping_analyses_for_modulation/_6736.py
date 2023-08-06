'''_6736.py

MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model import _2141
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6569
from mastapy.system_model.analyses_and_results.system_deflections import _2447
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6782
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'MeasurementComponentAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentAdvancedTimeSteppingAnalysisForModulation',)


class MeasurementComponentAdvancedTimeSteppingAnalysisForModulation(_6782.VirtualComponentAdvancedTimeSteppingAnalysisForModulation):
    '''MeasurementComponentAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2141.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6569.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6569.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2447.MeasurementComponentSystemDeflection':
        '''MeasurementComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2447.MeasurementComponentSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
