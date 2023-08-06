'''_5478.py

BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5476, _5477, _5483
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5348
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5483.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2192.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5476.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation]: 'BevelDifferentialGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5476.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bevel_differential_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5477.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'BevelDifferentialMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5477.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5348.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5348.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5348.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5348.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation))
        return value
