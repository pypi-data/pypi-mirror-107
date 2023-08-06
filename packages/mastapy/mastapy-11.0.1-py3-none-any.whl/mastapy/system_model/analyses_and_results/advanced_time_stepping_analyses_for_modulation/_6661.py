'''_6661.py

AdvancedTimeSteppingAnalysisForModulationOptions
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import (
    _6607, _6457, _6540, _6460,
    _6469, _6474, _6487, _6492,
    _6509, _6531, _6554, _6561,
    _6564, _6567, _6580, _6603,
    _6610, _6613, _6634, _6637
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results import _2358
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'AdvancedTimeSteppingAnalysisForModulationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedTimeSteppingAnalysisForModulationOptions',)


class AdvancedTimeSteppingAnalysisForModulationOptions(_0.APIBase):
    '''AdvancedTimeSteppingAnalysisForModulationOptions

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedTimeSteppingAnalysisForModulationOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_case_for_advanced_time_stepping_analysis_for_modulation_time_options(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptions' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(self.wrapped.LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptions) if self.wrapped.LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptions else None

    @load_case_for_advanced_time_stepping_analysis_for_modulation_time_options.setter
    def load_case_for_advanced_time_stepping_analysis_for_modulation_time_options(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptions = value

    @property
    def include_time_offset_for_steady_state(self) -> 'bool':
        '''bool: 'IncludeTimeOffsetForSteadyState' is the original name of this property.'''

        return self.wrapped.IncludeTimeOffsetForSteadyState

    @include_time_offset_for_steady_state.setter
    def include_time_offset_for_steady_state(self, value: 'bool'):
        self.wrapped.IncludeTimeOffsetForSteadyState = bool(value) if value else False

    @property
    def advanced_time_stepping_analysis_method(self) -> '_6457.AdvancedTimeSteppingAnalysisForModulationType':
        '''AdvancedTimeSteppingAnalysisForModulationType: 'AdvancedTimeSteppingAnalysisMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AdvancedTimeSteppingAnalysisMethod)
        return constructor.new(_6457.AdvancedTimeSteppingAnalysisForModulationType)(value) if value else None

    @advanced_time_stepping_analysis_method.setter
    def advanced_time_stepping_analysis_method(self, value: '_6457.AdvancedTimeSteppingAnalysisForModulationType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AdvancedTimeSteppingAnalysisMethod = value

    @property
    def number_of_steps_for_advanced_time_stepping_analysis(self) -> 'int':
        '''int: 'NumberOfStepsForAdvancedTimeSteppingAnalysis' is the original name of this property.'''

        return self.wrapped.NumberOfStepsForAdvancedTimeSteppingAnalysis

    @number_of_steps_for_advanced_time_stepping_analysis.setter
    def number_of_steps_for_advanced_time_stepping_analysis(self, value: 'int'):
        self.wrapped.NumberOfStepsForAdvancedTimeSteppingAnalysis = int(value) if value else 0

    @property
    def number_of_times_per_quasi_step(self) -> 'int':
        '''int: 'NumberOfTimesPerQuasiStep' is the original name of this property.'''

        return self.wrapped.NumberOfTimesPerQuasiStep

    @number_of_times_per_quasi_step.setter
    def number_of_times_per_quasi_step(self, value: 'int'):
        self.wrapped.NumberOfTimesPerQuasiStep = int(value) if value else 0

    @property
    def number_of_periods_for_advanced_time_stepping_analysis(self) -> 'float':
        '''float: 'NumberOfPeriodsForAdvancedTimeSteppingAnalysis' is the original name of this property.'''

        return self.wrapped.NumberOfPeriodsForAdvancedTimeSteppingAnalysis

    @number_of_periods_for_advanced_time_stepping_analysis.setter
    def number_of_periods_for_advanced_time_stepping_analysis(self, value: 'float'):
        self.wrapped.NumberOfPeriodsForAdvancedTimeSteppingAnalysis = float(value) if value else 0.0

    @property
    def time_options(self) -> '_2358.TimeOptions':
        '''TimeOptions: 'TimeOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2358.TimeOptions)(self.wrapped.TimeOptions) if self.wrapped.TimeOptions else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation(self) -> '_6540.GearSetLoadCase':
        '''GearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6540.GearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to GearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_agma_gleason_conical_gear_set_load_case(self) -> '_6460.AGMAGleasonConicalGearSetLoadCase':
        '''AGMAGleasonConicalGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6460.AGMAGleasonConicalGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to AGMAGleasonConicalGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_bevel_differential_gear_set_load_case(self) -> '_6469.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6469.BevelDifferentialGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to BevelDifferentialGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_bevel_gear_set_load_case(self) -> '_6474.BevelGearSetLoadCase':
        '''BevelGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6474.BevelGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to BevelGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_concept_gear_set_load_case(self) -> '_6487.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6487.ConceptGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to ConceptGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_conical_gear_set_load_case(self) -> '_6492.ConicalGearSetLoadCase':
        '''ConicalGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6492.ConicalGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to ConicalGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_cylindrical_gear_set_load_case(self) -> '_6509.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6509.CylindricalGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_face_gear_set_load_case(self) -> '_6531.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6531.FaceGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to FaceGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_hypoid_gear_set_load_case(self) -> '_6554.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6554.HypoidGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to HypoidGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self) -> '_6561.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        '''KlingelnbergCycloPalloidConicalGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6561.KlingelnbergCycloPalloidConicalGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to KlingelnbergCycloPalloidConicalGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self) -> '_6564.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6564.KlingelnbergCycloPalloidHypoidGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to KlingelnbergCycloPalloidHypoidGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self) -> '_6567.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6567.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_planetary_gear_set_load_case(self) -> '_6580.PlanetaryGearSetLoadCase':
        '''PlanetaryGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6580.PlanetaryGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to PlanetaryGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_spiral_bevel_gear_set_load_case(self) -> '_6603.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6603.SpiralBevelGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to SpiralBevelGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_straight_bevel_diff_gear_set_load_case(self) -> '_6610.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6610.StraightBevelDiffGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to StraightBevelDiffGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_straight_bevel_gear_set_load_case(self) -> '_6613.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6613.StraightBevelGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to StraightBevelGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_worm_gear_set_load_case(self) -> '_6634.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6634.WormGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to WormGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None

    @property
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation_of_type_zerol_bevel_gear_set_load_case(self) -> '_6637.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6637.ZerolBevelGearSetLoadCase.TYPE not in self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__mro__:
            raise CastException('Failed to cast gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation to ZerolBevelGearSetLoadCase. Expected: {}.'.format(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation.__class__)(self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation) if self.wrapped.GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation else None
