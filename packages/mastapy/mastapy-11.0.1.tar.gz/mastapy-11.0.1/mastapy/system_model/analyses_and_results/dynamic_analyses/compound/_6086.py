'''_6086.py

ConceptGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6084, _6085, _6115
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5956
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConceptGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundDynamicAnalysis',)


class ConceptGearSetCompoundDynamicAnalysis(_6115.GearSetCompoundDynamicAnalysis):
    '''ConceptGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundDynamicAnalysis.TYPE'):
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
    def concept_gears_compound_dynamic_analysis(self) -> 'List[_6084.ConceptGearCompoundDynamicAnalysis]':
        '''List[ConceptGearCompoundDynamicAnalysis]: 'ConceptGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundDynamicAnalysis, constructor.new(_6084.ConceptGearCompoundDynamicAnalysis))
        return value

    @property
    def concept_meshes_compound_dynamic_analysis(self) -> 'List[_6085.ConceptGearMeshCompoundDynamicAnalysis]':
        '''List[ConceptGearMeshCompoundDynamicAnalysis]: 'ConceptMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundDynamicAnalysis, constructor.new(_6085.ConceptGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5956.ConceptGearSetDynamicAnalysis]':
        '''List[ConceptGearSetDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5956.ConceptGearSetDynamicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5956.ConceptGearSetDynamicAnalysis]':
        '''List[ConceptGearSetDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5956.ConceptGearSetDynamicAnalysis))
        return value
