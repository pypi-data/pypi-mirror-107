'''_3950.py

TorqueConverterTurbineCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2286
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3821
from mastapy.system_model.analyses_and_results.power_flows.compound import _3869
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterTurbineCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundPowerFlow',)


class TorqueConverterTurbineCompoundPowerFlow(_3869.CouplingHalfCompoundPowerFlow):
    '''TorqueConverterTurbineCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundPowerFlow.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_3821.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3821.TorqueConverterTurbinePowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3821.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3821.TorqueConverterTurbinePowerFlow))
        return value
