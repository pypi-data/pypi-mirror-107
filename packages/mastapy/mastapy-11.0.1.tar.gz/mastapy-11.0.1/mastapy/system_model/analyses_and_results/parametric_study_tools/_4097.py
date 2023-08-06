'''_4097.py

TorqueConverterTurbineParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2286
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6625
from mastapy.system_model.analyses_and_results.system_deflections import _2498
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3997
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'TorqueConverterTurbineParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineParametricStudyTool',)


class TorqueConverterTurbineParametricStudyTool(_3997.CouplingHalfParametricStudyTool):
    '''TorqueConverterTurbineParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2286.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2286.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6625.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6625.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2498.TorqueConverterTurbineSystemDeflection]':
        '''List[TorqueConverterTurbineSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2498.TorqueConverterTurbineSystemDeflection))
        return value
