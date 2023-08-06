'''_2126.py

Connector
'''


from typing import Optional

from mastapy.system_model.connections_and_sockets import (
    _1957, _1947, _1948, _1955,
    _1960, _1961, _1963, _1964,
    _1965, _1966, _1967, _1969,
    _1970, _1971, _1974, _1975,
    _1953, _1946, _1949, _1950,
    _1954, _1962, _1968, _1973,
    _1976
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1991, _1980, _1982, _1984,
    _1986, _1988, _1990, _1992,
    _1994, _1996, _1999, _2000,
    _2001, _2004, _2006, _2008,
    _2010, _2012
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2014, _2015, _2017, _2018,
    _2020, _2021, _2016, _2019,
    _2022
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2024, _2026, _2028, _2030,
    _2032, _2034, _2035, _2023,
    _2025, _2027, _2029, _2031,
    _2033
)
from mastapy.system_model.part_model import (
    _2115, _2124, _2123, _2142
)
from mastapy.system_model.part_model.shaft_model import _2159
from mastapy.system_model.part_model.cycloidal import _2245
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2142.MountableComponent):
    '''Connector

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_socket(self) -> '_1957.CylindricalSocket':
        '''CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.CylindricalSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_bearing_inner_socket(self) -> '_1947.BearingInnerSocket':
        '''BearingInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.BearingInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_1948.BearingOuterSocket':
        '''BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.BearingOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_1955.CVTPulleySocket':
        '''CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.CVTPulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_1960.InnerShaftSocket':
        '''InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.InnerShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_1961.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.InnerShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_mountable_component_inner_socket(self) -> '_1963.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.MountableComponentInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_mountable_component_outer_socket(self) -> '_1964.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.MountableComponentOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_mountable_component_socket(self) -> '_1965.MountableComponentSocket':
        '''MountableComponentSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.MountableComponentSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_1966.OuterShaftSocket':
        '''OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.OuterShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_outer_shaft_socket_base(self) -> '_1967.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1967.OuterShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_1969.PlanetarySocket':
        '''PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.PlanetarySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_1970.PlanetarySocketBase':
        '''PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.PlanetarySocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_1971.PulleySocket':
        '''PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1971.PulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_1974.RollingRingSocket':
        '''RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.RollingRingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_1975.ShaftSocket':
        '''ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.ShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_1991.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.CylindricalGearTeethSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2014.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2015.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2017.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.CycloidalDiscInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2018.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.CycloidalDiscOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2020.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_2021.RingPinsSocket':
        '''RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.RingPinsSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_2024.ClutchSocket':
        '''ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.ClutchSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_2026.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.ConceptCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_2028.CouplingSocket':
        '''CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.CouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2030.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.PartToPartShearCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2032.SpringDamperSocket':
        '''SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.SpringDamperSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2034.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.TorqueConverterPumpSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2035.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.TorqueConverterTurbineSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_connection(self) -> '_1953.Connection':
        '''Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.Connection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1946.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_1949.BeltConnection':
        '''BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.BeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_1950.CoaxialConnection':
        '''CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1950.CoaxialConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_1954.CVTBeltConnection':
        '''CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1954.CVTBeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_1962.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.InterMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_1968.PlanetaryConnection':
        '''PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetaryConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_1973.RollingRingConnection':
        '''RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.RollingRingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_1976.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.ShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_1980.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_1982.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelDifferentialGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_1984.BevelGearMesh':
        '''BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.BevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_1986.ConceptGearMesh':
        '''ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConceptGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_1988.ConicalGearMesh':
        '''ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.ConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_1990.CylindricalGearMesh':
        '''CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CylindricalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_1992.FaceGearMesh':
        '''FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.FaceGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_1994.GearMesh':
        '''GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.GearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_1996.HypoidGearMesh':
        '''HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.HypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1999.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2000.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2001.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2004.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.SpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2006.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelDiffGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_2008.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.StraightBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_2010.WormGearMesh':
        '''WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.WormGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2012.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.ZerolBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2016.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2019.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_2022.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.RingPinsToDiscConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_2023.ClutchConnection':
        '''ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ClutchConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_2025.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.ConceptCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_2027.CouplingConnection':
        '''CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.CouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2029.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.PartToPartShearCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2031.SpringDamperConnection':
        '''SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.SpringDamperConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2033.TorqueConverterConnection':
        '''TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_component(self) -> '_2115.AbstractShaft':
        '''AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.AbstractShaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    @property
    def outer_component_of_type_shaft(self) -> '_2159.Shaft':
        '''Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.Shaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2245.CycloidalDisc':
        '''CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.CycloidalDisc.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    def house_in(self, shaft: '_2115.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_1953.Connection':
        ''' 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def try_house_in(self, shaft: '_2115.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2124.ComponentsConnectedResult':
        ''' 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_component(self, component: '_2123.Component') -> '_2115.AbstractShaft':
        ''' 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        '''

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
