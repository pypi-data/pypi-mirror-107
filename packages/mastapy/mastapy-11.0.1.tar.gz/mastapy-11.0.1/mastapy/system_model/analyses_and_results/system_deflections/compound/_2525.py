'''_2525.py

AssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2113, _2152
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis import _45
from mastapy.shafts import _37
from mastapy.gears.analysis import _1136
from mastapy.system_model.analyses_and_results.system_deflections import _2366
from mastapy.system_model.analyses_and_results.system_deflections.compound import (
    _2526, _2528, _2531, _2537,
    _2538, _2539, _2544, _2549,
    _2559, _2561, _2563, _2567,
    _2574, _2575, _2576, _2583,
    _2590, _2593, _2594, _2595,
    _2597, _2599, _2604, _2605,
    _2606, _2616, _2608, _2610,
    _2614, _2621, _2622, _2627,
    _2630, _2633, _2637, _2641,
    _2645, _2648, _2518
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSystemDeflection',)


class AssemblyCompoundSystemDeflection(_2518.AbstractAssemblyCompoundSystemDeflection):
    '''AssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def overall_duty_cycle_shaft_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleShaftReliability

    @property
    def overall_duty_cycle_bearing_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleBearingReliability

    @property
    def overall_duty_cycle_gear_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleGearReliability

    @property
    def overall_oil_seal_duty_cycle_reliability(self) -> 'float':
        '''float: 'OverallOilSealDutyCycleReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallOilSealDutyCycleReliability

    @property
    def overall_system_reliability(self) -> 'float':
        '''float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallSystemReliability

    @property
    def component_design(self) -> '_2113.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2113.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2113.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2113.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def analysis_settings(self) -> '_45.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_45.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def rating_for_all_gear_sets(self) -> '_1136.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1136.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2366.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2366.AssemblySystemDeflection))
        return value

    @property
    def bearings(self) -> 'List[_2526.BearingCompoundSystemDeflection]':
        '''List[BearingCompoundSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2526.BearingCompoundSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_2528.BeltDriveCompoundSystemDeflection]':
        '''List[BeltDriveCompoundSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2528.BeltDriveCompoundSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2531.BevelDifferentialGearSetCompoundSystemDeflection]':
        '''List[BevelDifferentialGearSetCompoundSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2531.BevelDifferentialGearSetCompoundSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_2537.BoltCompoundSystemDeflection]':
        '''List[BoltCompoundSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2537.BoltCompoundSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_2538.BoltedJointCompoundSystemDeflection]':
        '''List[BoltedJointCompoundSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2538.BoltedJointCompoundSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_2539.ClutchCompoundSystemDeflection]':
        '''List[ClutchCompoundSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2539.ClutchCompoundSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_2544.ConceptCouplingCompoundSystemDeflection]':
        '''List[ConceptCouplingCompoundSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2544.ConceptCouplingCompoundSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2549.ConceptGearSetCompoundSystemDeflection]':
        '''List[ConceptGearSetCompoundSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2549.ConceptGearSetCompoundSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_2559.CVTCompoundSystemDeflection]':
        '''List[CVTCompoundSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2559.CVTCompoundSystemDeflection))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_2561.CycloidalAssemblyCompoundSystemDeflection]':
        '''List[CycloidalAssemblyCompoundSystemDeflection]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_2561.CycloidalAssemblyCompoundSystemDeflection))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_2563.CycloidalDiscCompoundSystemDeflection]':
        '''List[CycloidalDiscCompoundSystemDeflection]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_2563.CycloidalDiscCompoundSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2567.CylindricalGearSetCompoundSystemDeflection]':
        '''List[CylindricalGearSetCompoundSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2567.CylindricalGearSetCompoundSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2574.FaceGearSetCompoundSystemDeflection]':
        '''List[FaceGearSetCompoundSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2574.FaceGearSetCompoundSystemDeflection))
        return value

    @property
    def fe_parts(self) -> 'List[_2575.FEPartCompoundSystemDeflection]':
        '''List[FEPartCompoundSystemDeflection]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_2575.FEPartCompoundSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2576.FlexiblePinAssemblyCompoundSystemDeflection]':
        '''List[FlexiblePinAssemblyCompoundSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2576.FlexiblePinAssemblyCompoundSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2583.HypoidGearSetCompoundSystemDeflection]':
        '''List[HypoidGearSetCompoundSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2583.HypoidGearSetCompoundSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2590.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2590.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2593.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2593.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_2594.MassDiscCompoundSystemDeflection]':
        '''List[MassDiscCompoundSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2594.MassDiscCompoundSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_2595.MeasurementComponentCompoundSystemDeflection]':
        '''List[MeasurementComponentCompoundSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2595.MeasurementComponentCompoundSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_2597.OilSealCompoundSystemDeflection]':
        '''List[OilSealCompoundSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2597.OilSealCompoundSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2599.PartToPartShearCouplingCompoundSystemDeflection]':
        '''List[PartToPartShearCouplingCompoundSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2599.PartToPartShearCouplingCompoundSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_2604.PlanetCarrierCompoundSystemDeflection]':
        '''List[PlanetCarrierCompoundSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2604.PlanetCarrierCompoundSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_2605.PointLoadCompoundSystemDeflection]':
        '''List[PointLoadCompoundSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2605.PointLoadCompoundSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_2606.PowerLoadCompoundSystemDeflection]':
        '''List[PowerLoadCompoundSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2606.PowerLoadCompoundSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2616.ShaftHubConnectionCompoundSystemDeflection]':
        '''List[ShaftHubConnectionCompoundSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2616.ShaftHubConnectionCompoundSystemDeflection))
        return value

    @property
    def ring_pins(self) -> 'List[_2608.RingPinsCompoundSystemDeflection]':
        '''List[RingPinsCompoundSystemDeflection]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_2608.RingPinsCompoundSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2610.RollingRingAssemblyCompoundSystemDeflection]':
        '''List[RollingRingAssemblyCompoundSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2610.RollingRingAssemblyCompoundSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_2614.ShaftCompoundSystemDeflection]':
        '''List[ShaftCompoundSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2614.ShaftCompoundSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2621.SpiralBevelGearSetCompoundSystemDeflection]':
        '''List[SpiralBevelGearSetCompoundSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2621.SpiralBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_2622.SpringDamperCompoundSystemDeflection]':
        '''List[SpringDamperCompoundSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2622.SpringDamperCompoundSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2627.StraightBevelDiffGearSetCompoundSystemDeflection]':
        '''List[StraightBevelDiffGearSetCompoundSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2627.StraightBevelDiffGearSetCompoundSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2630.StraightBevelGearSetCompoundSystemDeflection]':
        '''List[StraightBevelGearSetCompoundSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2630.StraightBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_2633.SynchroniserCompoundSystemDeflection]':
        '''List[SynchroniserCompoundSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2633.SynchroniserCompoundSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_2637.TorqueConverterCompoundSystemDeflection]':
        '''List[TorqueConverterCompoundSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2637.TorqueConverterCompoundSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2641.UnbalancedMassCompoundSystemDeflection]':
        '''List[UnbalancedMassCompoundSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2641.UnbalancedMassCompoundSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2645.WormGearSetCompoundSystemDeflection]':
        '''List[WormGearSetCompoundSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2645.WormGearSetCompoundSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2648.ZerolBevelGearSetCompoundSystemDeflection]':
        '''List[ZerolBevelGearSetCompoundSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2648.ZerolBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def rolling_bearings(self) -> 'List[_2526.BearingCompoundSystemDeflection]':
        '''List[BearingCompoundSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingBearings, constructor.new(_2526.BearingCompoundSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2366.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2366.AssemblySystemDeflection))
        return value
