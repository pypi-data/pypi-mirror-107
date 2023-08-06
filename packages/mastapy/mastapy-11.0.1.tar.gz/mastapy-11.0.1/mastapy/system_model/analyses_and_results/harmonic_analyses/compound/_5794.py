'''_5794.py

AssemblyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2113, _2152
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5602
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
    _5795, _5797, _5800, _5806,
    _5807, _5808, _5813, _5818,
    _5828, _5830, _5832, _5836,
    _5842, _5843, _5844, _5851,
    _5858, _5861, _5862, _5863,
    _5865, _5867, _5872, _5873,
    _5874, _5883, _5876, _5878,
    _5882, _5888, _5889, _5894,
    _5897, _5900, _5904, _5908,
    _5912, _5915, _5787
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundHarmonicAnalysis',)


class AssemblyCompoundHarmonicAnalysis(_5787.AbstractAssemblyCompoundHarmonicAnalysis):
    '''AssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_analysis_cases_ready(self) -> 'List[_5602.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5602.AssemblyHarmonicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5795.BearingCompoundHarmonicAnalysis]':
        '''List[BearingCompoundHarmonicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5795.BearingCompoundHarmonicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5797.BeltDriveCompoundHarmonicAnalysis]':
        '''List[BeltDriveCompoundHarmonicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5797.BeltDriveCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5800.BevelDifferentialGearSetCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundHarmonicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5800.BevelDifferentialGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5806.BoltCompoundHarmonicAnalysis]':
        '''List[BoltCompoundHarmonicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5806.BoltCompoundHarmonicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5807.BoltedJointCompoundHarmonicAnalysis]':
        '''List[BoltedJointCompoundHarmonicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5807.BoltedJointCompoundHarmonicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5808.ClutchCompoundHarmonicAnalysis]':
        '''List[ClutchCompoundHarmonicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5808.ClutchCompoundHarmonicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5813.ConceptCouplingCompoundHarmonicAnalysis]':
        '''List[ConceptCouplingCompoundHarmonicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5813.ConceptCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5818.ConceptGearSetCompoundHarmonicAnalysis]':
        '''List[ConceptGearSetCompoundHarmonicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5818.ConceptGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5828.CVTCompoundHarmonicAnalysis]':
        '''List[CVTCompoundHarmonicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5828.CVTCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5830.CycloidalAssemblyCompoundHarmonicAnalysis]':
        '''List[CycloidalAssemblyCompoundHarmonicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5830.CycloidalAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5832.CycloidalDiscCompoundHarmonicAnalysis]':
        '''List[CycloidalDiscCompoundHarmonicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5832.CycloidalDiscCompoundHarmonicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5836.CylindricalGearSetCompoundHarmonicAnalysis]':
        '''List[CylindricalGearSetCompoundHarmonicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5836.CylindricalGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5842.FaceGearSetCompoundHarmonicAnalysis]':
        '''List[FaceGearSetCompoundHarmonicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5842.FaceGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5843.FEPartCompoundHarmonicAnalysis]':
        '''List[FEPartCompoundHarmonicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5843.FEPartCompoundHarmonicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5844.FlexiblePinAssemblyCompoundHarmonicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundHarmonicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5844.FlexiblePinAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5851.HypoidGearSetCompoundHarmonicAnalysis]':
        '''List[HypoidGearSetCompoundHarmonicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5851.HypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5858.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5858.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5861.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5861.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5862.MassDiscCompoundHarmonicAnalysis]':
        '''List[MassDiscCompoundHarmonicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5862.MassDiscCompoundHarmonicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5863.MeasurementComponentCompoundHarmonicAnalysis]':
        '''List[MeasurementComponentCompoundHarmonicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5863.MeasurementComponentCompoundHarmonicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5865.OilSealCompoundHarmonicAnalysis]':
        '''List[OilSealCompoundHarmonicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5865.OilSealCompoundHarmonicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5867.PartToPartShearCouplingCompoundHarmonicAnalysis]':
        '''List[PartToPartShearCouplingCompoundHarmonicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5867.PartToPartShearCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5872.PlanetCarrierCompoundHarmonicAnalysis]':
        '''List[PlanetCarrierCompoundHarmonicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5872.PlanetCarrierCompoundHarmonicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5873.PointLoadCompoundHarmonicAnalysis]':
        '''List[PointLoadCompoundHarmonicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5873.PointLoadCompoundHarmonicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5874.PowerLoadCompoundHarmonicAnalysis]':
        '''List[PowerLoadCompoundHarmonicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5874.PowerLoadCompoundHarmonicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5883.ShaftHubConnectionCompoundHarmonicAnalysis]':
        '''List[ShaftHubConnectionCompoundHarmonicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5883.ShaftHubConnectionCompoundHarmonicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5876.RingPinsCompoundHarmonicAnalysis]':
        '''List[RingPinsCompoundHarmonicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5876.RingPinsCompoundHarmonicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5878.RollingRingAssemblyCompoundHarmonicAnalysis]':
        '''List[RollingRingAssemblyCompoundHarmonicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5878.RollingRingAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5882.ShaftCompoundHarmonicAnalysis]':
        '''List[ShaftCompoundHarmonicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5882.ShaftCompoundHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5888.SpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearSetCompoundHarmonicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5888.SpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5889.SpringDamperCompoundHarmonicAnalysis]':
        '''List[SpringDamperCompoundHarmonicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5889.SpringDamperCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5894.StraightBevelDiffGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundHarmonicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5894.StraightBevelDiffGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5897.StraightBevelGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearSetCompoundHarmonicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5897.StraightBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5900.SynchroniserCompoundHarmonicAnalysis]':
        '''List[SynchroniserCompoundHarmonicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5900.SynchroniserCompoundHarmonicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5904.TorqueConverterCompoundHarmonicAnalysis]':
        '''List[TorqueConverterCompoundHarmonicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5904.TorqueConverterCompoundHarmonicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5908.UnbalancedMassCompoundHarmonicAnalysis]':
        '''List[UnbalancedMassCompoundHarmonicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5908.UnbalancedMassCompoundHarmonicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5912.WormGearSetCompoundHarmonicAnalysis]':
        '''List[WormGearSetCompoundHarmonicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5912.WormGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5915.ZerolBevelGearSetCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearSetCompoundHarmonicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5915.ZerolBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5602.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5602.AssemblyHarmonicAnalysis))
        return value
