'''_3732.py

ConnectionPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1953, _1946, _1949, _1950,
    _1954, _1962, _1968, _1973,
    _1976
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1980, _1982, _1984, _1986,
    _1988, _1990, _1992, _1994,
    _1996, _1999, _2000, _2001,
    _2004, _2006, _2008, _2010,
    _2012
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2016, _2019, _2022
from mastapy.system_model.connections_and_sockets.couplings import (
    _2023, _2025, _2027, _2029,
    _2031, _2033
)
from mastapy.system_model.analyses_and_results.power_flows import _3785
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2396, _2362, _2363, _2368,
    _2370, _2375, _2380, _2383,
    _2386, _2389, _2393, _2398,
    _2401, _2405, _2406, _2408,
    _2409, _2410, _2421, _2426,
    _2430, _2434, _2435, _2438,
    _2441, _2453, _2456, _2462,
    _2465, _2472, _2474, _2477,
    _2480, _2483, _2495, _2503,
    _2506
)
from mastapy.system_model.analyses_and_results.analysis_cases import _7189
from mastapy._internal.python_net import python_net_import

_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionPowerFlow',)


class ConnectionPowerFlow(_7189.ConnectionStaticLoadAnalysisCase):
    '''ConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def component_design(self) -> '_1953.Connection':
        '''Connection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.Connection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1946.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_connection(self) -> '_1949.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.BeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coaxial_connection(self) -> '_1950.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1950.CoaxialConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_belt_connection(self) -> '_1954.CVTBeltConnection':
        '''CVTBeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1954.CVTBeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_inter_mountable_component_connection(self) -> '_1962.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.InterMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_connection(self) -> '_1968.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetaryConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_connection(self) -> '_1973.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.RollingRingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_to_mountable_component_connection(self) -> '_1976.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1980.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_mesh(self) -> '_1982.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelDifferentialGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear_mesh(self) -> '_1984.BevelGearMesh':
        '''BevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.BevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_mesh(self) -> '_1986.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConceptGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear_mesh(self) -> '_1988.ConicalGearMesh':
        '''ConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.ConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_mesh(self) -> '_1990.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CylindricalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_mesh(self) -> '_1992.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.FaceGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear_mesh(self) -> '_1994.GearMesh':
        '''GearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.GearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_mesh(self) -> '_1996.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.HypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1999.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2000.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2001.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_mesh(self) -> '_2004.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.SpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_2006.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_mesh(self) -> '_2008.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.StraightBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_mesh(self) -> '_2010.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.WormGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_mesh(self) -> '_2012.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.ZerolBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2016.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2019.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_ring_pins_to_disc_connection(self) -> '_2022.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.RingPinsToDiscConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_connection(self) -> '_2023.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ClutchConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_connection(self) -> '_2025.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.ConceptCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling_connection(self) -> '_2027.CouplingConnection':
        '''CouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.CouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2029.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_connection(self) -> '_2031.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.SpringDamperConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_connection(self) -> '_2033.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1953.Connection':
        '''Connection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.Connection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to Connection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1946.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_belt_connection(self) -> '_1949.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coaxial_connection(self) -> '_1950.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1950.CoaxialConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cvt_belt_connection(self) -> '_1954.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1954.CVTBeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_inter_mountable_component_connection(self) -> '_1962.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.InterMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_planetary_connection(self) -> '_1968.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetaryConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_rolling_ring_connection(self) -> '_1973.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.RollingRingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_shaft_to_mountable_component_connection(self) -> '_1976.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1980.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1982.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1984.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1986.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConceptGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_conical_gear_mesh(self) -> '_1988.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1990.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CylindricalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1992.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.FaceGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_gear_mesh(self) -> '_1994.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.GearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to GearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1996.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1999.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2000.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2001.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_2004.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_2006.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_2008.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_2010.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.WormGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_2012.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2016.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2019.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_ring_pins_to_disc_connection(self) -> '_2022.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.RingPinsToDiscConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_2023.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ClutchConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_2025.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.ConceptCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coupling_connection(self) -> '_2027.CouplingConnection':
        '''CouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.CouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2029.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_2031.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.SpringDamperConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_2033.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow(self) -> '_3785.PowerFlow':
        '''PowerFlow: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3785.PowerFlow)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def torsional_system_deflection_analysis(self) -> '_2396.ConnectionSystemDeflection':
        '''ConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2396.ConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_abstract_shaft_to_mountable_component_connection_system_deflection(self) -> '_2362.AbstractShaftToMountableComponentConnectionSystemDeflection':
        '''AbstractShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2362.AbstractShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AbstractShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2363.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2363.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_belt_connection_system_deflection(self) -> '_2368.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2368.BeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2370.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2370.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_gear_mesh_system_deflection(self) -> '_2375.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2375.BevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_clutch_connection_system_deflection(self) -> '_2380.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2380.ClutchConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ClutchConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coaxial_connection_system_deflection(self) -> '_2383.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2383.CoaxialConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CoaxialConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_coupling_connection_system_deflection(self) -> '_2386.ConceptCouplingConnectionSystemDeflection':
        '''ConceptCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2386.ConceptCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_gear_mesh_system_deflection(self) -> '_2389.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2389.ConceptGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_conical_gear_mesh_system_deflection(self) -> '_2393.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2393.ConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coupling_connection_system_deflection(self) -> '_2398.CouplingConnectionSystemDeflection':
        '''CouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2398.CouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cvt_belt_connection_system_deflection(self) -> '_2401.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2401.CVTBeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CVTBeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_central_bearing_connection_system_deflection(self) -> '_2405.CycloidalDiscCentralBearingConnectionSystemDeflection':
        '''CycloidalDiscCentralBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2405.CycloidalDiscCentralBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscCentralBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_planetary_bearing_connection_system_deflection(self) -> '_2406.CycloidalDiscPlanetaryBearingConnectionSystemDeflection':
        '''CycloidalDiscPlanetaryBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2406.CycloidalDiscPlanetaryBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscPlanetaryBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2408.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2408.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2409.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2409.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2410.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2410.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_face_gear_mesh_system_deflection(self) -> '_2421.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2421.FaceGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_gear_mesh_system_deflection(self) -> '_2426.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2426.GearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to GearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2430.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2430.HypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_inter_mountable_component_connection_system_deflection(self) -> '_2434.InterMountableComponentConnectionSystemDeflection':
        '''InterMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2434.InterMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to InterMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2435.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2435.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2438.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2438.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2441.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2441.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_part_to_part_shear_coupling_connection_system_deflection(self) -> '_2453.PartToPartShearCouplingConnectionSystemDeflection':
        '''PartToPartShearCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2453.PartToPartShearCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PartToPartShearCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_planetary_connection_system_deflection(self) -> '_2456.PlanetaryConnectionSystemDeflection':
        '''PlanetaryConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2456.PlanetaryConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PlanetaryConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_ring_pins_to_disc_connection_system_deflection(self) -> '_2462.RingPinsToDiscConnectionSystemDeflection':
        '''RingPinsToDiscConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2462.RingPinsToDiscConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RingPinsToDiscConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_rolling_ring_connection_system_deflection(self) -> '_2465.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2465.RollingRingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RollingRingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_shaft_to_mountable_component_connection_system_deflection(self) -> '_2472.ShaftToMountableComponentConnectionSystemDeflection':
        '''ShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2472.ShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2474.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2474.SpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spring_damper_connection_system_deflection(self) -> '_2477.SpringDamperConnectionSystemDeflection':
        '''SpringDamperConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2477.SpringDamperConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpringDamperConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2480.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2480.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2483.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2483.StraightBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_torque_converter_connection_system_deflection(self) -> '_2495.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2495.TorqueConverterConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to TorqueConverterConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_worm_gear_mesh_system_deflection(self) -> '_2503.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2503.WormGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2506.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2506.ZerolBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None
