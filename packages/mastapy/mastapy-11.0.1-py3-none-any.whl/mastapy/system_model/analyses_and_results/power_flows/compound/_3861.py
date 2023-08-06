'''_3861.py

ConceptGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3859, _3860, _3890
from mastapy.system_model.analyses_and_results.power_flows import _3728
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConceptGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundPowerFlow',)


class ConceptGearSetCompoundPowerFlow(_3890.GearSetCompoundPowerFlow):
    '''ConceptGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2198.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2198.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_power_flow(self) -> 'List[_3859.ConceptGearCompoundPowerFlow]':
        '''List[ConceptGearCompoundPowerFlow]: 'ConceptGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundPowerFlow, constructor.new(_3859.ConceptGearCompoundPowerFlow))
        return value

    @property
    def concept_meshes_compound_power_flow(self) -> 'List[_3860.ConceptGearMeshCompoundPowerFlow]':
        '''List[ConceptGearMeshCompoundPowerFlow]: 'ConceptMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundPowerFlow, constructor.new(_3860.ConceptGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3728.ConceptGearSetPowerFlow]':
        '''List[ConceptGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3728.ConceptGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3728.ConceptGearSetPowerFlow]':
        '''List[ConceptGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3728.ConceptGearSetPowerFlow))
        return value
