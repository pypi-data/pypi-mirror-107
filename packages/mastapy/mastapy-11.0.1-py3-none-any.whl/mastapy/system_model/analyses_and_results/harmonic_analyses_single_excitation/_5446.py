'''_5446.py

StraightBevelGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2224
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6613
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5444, _5445, _5353
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'StraightBevelGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetHarmonicAnalysisOfSingleExcitation',)


class StraightBevelGearSetHarmonicAnalysisOfSingleExcitation(_5353.BevelGearSetHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2224.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6613.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6613.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5444.StraightBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearHarmonicAnalysisOfSingleExcitation]: 'StraightBevelGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5444.StraightBevelGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5445.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation]: 'StraightBevelMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5445.StraightBevelGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
