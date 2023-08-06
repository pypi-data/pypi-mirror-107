'''_1362.py

MeasurementSettings
'''


from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.utility.units_and_measurements import _1361
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.utility.units_and_measurements.measurements import (
    _1368, _1369, _1370, _1371,
    _1372, _1373, _1374, _1375,
    _1376, _1377, _1378, _1379,
    _1380, _1381, _1382, _1383,
    _1384, _1385, _1386, _1387,
    _1388, _1389, _1390, _1391,
    _1392, _1393, _1394, _1395,
    _1396, _1397, _1398, _1399,
    _1400, _1401, _1402, _1403,
    _1404, _1405, _1406, _1407,
    _1408, _1409, _1410, _1411,
    _1412, _1413, _1414, _1415,
    _1416, _1417, _1418, _1419,
    _1420, _1421, _1422, _1423,
    _1424, _1425, _1426, _1427,
    _1428, _1429, _1430, _1431,
    _1432, _1433, _1434, _1435,
    _1436, _1437, _1438, _1439,
    _1440, _1441, _1442, _1443,
    _1444, _1445, _1446, _1447,
    _1448, _1449, _1450, _1451,
    _1452, _1453, _1454, _1455,
    _1456, _1457, _1458, _1459,
    _1460, _1461, _1462, _1463,
    _1464, _1465, _1466, _1467,
    _1468, _1469, _1470, _1471,
    _1472, _1473, _1474, _1475
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility import _1350
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_SETTINGS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'MeasurementSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementSettings',)


class MeasurementSettings(_1350.PerMachineSettings):
    '''MeasurementSettings

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_measurement(self) -> 'list_with_selected_item.ListWithSelectedItem_MeasurementBase':
        '''list_with_selected_item.ListWithSelectedItem_MeasurementBase: 'SelectedMeasurement' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_MeasurementBase)(self.wrapped.SelectedMeasurement) if self.wrapped.SelectedMeasurement else None

    @selected_measurement.setter
    def selected_measurement(self, value: 'list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedMeasurement = value

    @property
    def sample_input(self) -> 'str':
        '''str: 'SampleInput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SampleInput

    @property
    def sample_output(self) -> 'str':
        '''str: 'SampleOutput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SampleOutput

    @property
    def number_decimal_separator(self) -> 'str':
        '''str: 'NumberDecimalSeparator' is the original name of this property.'''

        return self.wrapped.NumberDecimalSeparator

    @number_decimal_separator.setter
    def number_decimal_separator(self, value: 'str'):
        self.wrapped.NumberDecimalSeparator = str(value) if value else None

    @property
    def number_group_separator(self) -> 'str':
        '''str: 'NumberGroupSeparator' is the original name of this property.'''

        return self.wrapped.NumberGroupSeparator

    @number_group_separator.setter
    def number_group_separator(self, value: 'str'):
        self.wrapped.NumberGroupSeparator = str(value) if value else None

    @property
    def small_number_cutoff(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SmallNumberCutoff' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SmallNumberCutoff) if self.wrapped.SmallNumberCutoff else None

    @small_number_cutoff.setter
    def small_number_cutoff(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SmallNumberCutoff = value

    @property
    def large_number_cutoff(self) -> 'float':
        '''float: 'LargeNumberCutoff' is the original name of this property.'''

        return self.wrapped.LargeNumberCutoff

    @large_number_cutoff.setter
    def large_number_cutoff(self, value: 'float'):
        self.wrapped.LargeNumberCutoff = float(value) if value else 0.0

    @property
    def show_trailing_zeros(self) -> 'bool':
        '''bool: 'ShowTrailingZeros' is the original name of this property.'''

        return self.wrapped.ShowTrailingZeros

    @show_trailing_zeros.setter
    def show_trailing_zeros(self, value: 'bool'):
        self.wrapped.ShowTrailingZeros = bool(value) if value else False

    @property
    def current_selected_measurement(self) -> '_1361.MeasurementBase':
        '''MeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1361.MeasurementBase.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MeasurementBase. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_acceleration(self) -> '_1368.Acceleration':
        '''Acceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1368.Acceleration.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Acceleration. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle(self) -> '_1369.Angle':
        '''Angle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1369.Angle.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Angle. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_per_unit_temperature(self) -> '_1370.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1370.AnglePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AnglePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_small(self) -> '_1371.AngleSmall':
        '''AngleSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1371.AngleSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_very_small(self) -> '_1372.AngleVerySmall':
        '''AngleVerySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1372.AngleVerySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleVerySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_acceleration(self) -> '_1373.AngularAcceleration':
        '''AngularAcceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1373.AngularAcceleration.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularAcceleration. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_compliance(self) -> '_1374.AngularCompliance':
        '''AngularCompliance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1374.AngularCompliance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularCompliance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_jerk(self) -> '_1375.AngularJerk':
        '''AngularJerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1375.AngularJerk.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularJerk. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_stiffness(self) -> '_1376.AngularStiffness':
        '''AngularStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1376.AngularStiffness.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularStiffness. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_velocity(self) -> '_1377.AngularVelocity':
        '''AngularVelocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1377.AngularVelocity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularVelocity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_area(self) -> '_1378.Area':
        '''Area: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1378.Area.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Area. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_area_small(self) -> '_1379.AreaSmall':
        '''AreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1379.AreaSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AreaSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_cycles(self) -> '_1380.Cycles':
        '''Cycles: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1380.Cycles.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Cycles. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_damage(self) -> '_1381.Damage':
        '''Damage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1381.Damage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Damage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_damage_rate(self) -> '_1382.DamageRate':
        '''DamageRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1382.DamageRate.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DamageRate. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_data_size(self) -> '_1383.DataSize':
        '''DataSize: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1383.DataSize.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DataSize. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_decibel(self) -> '_1384.Decibel':
        '''Decibel: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1384.Decibel.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Decibel. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_density(self) -> '_1385.Density':
        '''Density: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1385.Density.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Density. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy(self) -> '_1386.Energy':
        '''Energy: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1386.Energy.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Energy. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area(self) -> '_1387.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1387.EnergyPerUnitArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area_small(self) -> '_1388.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1388.EnergyPerUnitAreaSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_small(self) -> '_1389.EnergySmall':
        '''EnergySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1389.EnergySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_enum(self) -> '_1390.Enum':
        '''Enum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1390.Enum.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Enum. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_flow_rate(self) -> '_1391.FlowRate':
        '''FlowRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1391.FlowRate.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FlowRate. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force(self) -> '_1392.Force':
        '''Force: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1392.Force.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Force. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_length(self) -> '_1393.ForcePerUnitLength':
        '''ForcePerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1393.ForcePerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_pressure(self) -> '_1394.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1394.ForcePerUnitPressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitPressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_temperature(self) -> '_1395.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1395.ForcePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fraction_measurement_base(self) -> '_1396.FractionMeasurementBase':
        '''FractionMeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1396.FractionMeasurementBase.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FractionMeasurementBase. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_frequency(self) -> '_1397.Frequency':
        '''Frequency: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1397.Frequency.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Frequency. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fuel_consumption_engine(self) -> '_1398.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1398.FuelConsumptionEngine.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelConsumptionEngine. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fuel_efficiency_vehicle(self) -> '_1399.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1399.FuelEfficiencyVehicle.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelEfficiencyVehicle. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_gradient(self) -> '_1400.Gradient':
        '''Gradient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1400.Gradient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Gradient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_conductivity(self) -> '_1401.HeatConductivity':
        '''HeatConductivity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1401.HeatConductivity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatConductivity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer(self) -> '_1402.HeatTransfer':
        '''HeatTransfer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1402.HeatTransfer.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransfer. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1403.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1403.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer_resistance(self) -> '_1404.HeatTransferResistance':
        '''HeatTransferResistance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1404.HeatTransferResistance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferResistance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_impulse(self) -> '_1405.Impulse':
        '''Impulse: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1405.Impulse.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Impulse. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_index(self) -> '_1406.Index':
        '''Index: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1406.Index.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Index. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_integer(self) -> '_1407.Integer':
        '''Integer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1407.Integer.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Integer. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_inverse_short_length(self) -> '_1408.InverseShortLength':
        '''InverseShortLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1408.InverseShortLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_inverse_short_time(self) -> '_1409.InverseShortTime':
        '''InverseShortTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1409.InverseShortTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_jerk(self) -> '_1410.Jerk':
        '''Jerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1410.Jerk.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Jerk. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_kinematic_viscosity(self) -> '_1411.KinematicViscosity':
        '''KinematicViscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1411.KinematicViscosity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to KinematicViscosity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_long(self) -> '_1412.LengthLong':
        '''LengthLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1412.LengthLong.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthLong. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_medium(self) -> '_1413.LengthMedium':
        '''LengthMedium: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1413.LengthMedium.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthMedium. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_per_unit_temperature(self) -> '_1414.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1414.LengthPerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthPerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_short(self) -> '_1415.LengthShort':
        '''LengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1415.LengthShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_to_the_fourth(self) -> '_1416.LengthToTheFourth':
        '''LengthToTheFourth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1416.LengthToTheFourth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthToTheFourth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_long(self) -> '_1417.LengthVeryLong':
        '''LengthVeryLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1417.LengthVeryLong.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryLong. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_short(self) -> '_1418.LengthVeryShort':
        '''LengthVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1418.LengthVeryShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_short_per_length_short(self) -> '_1419.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1419.LengthVeryShortPerLengthShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_angular_damping(self) -> '_1420.LinearAngularDamping':
        '''LinearAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1420.LinearAngularDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1421.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1421.LinearAngularStiffnessCrossTerm.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_damping(self) -> '_1422.LinearDamping':
        '''LinearDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1422.LinearDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_flexibility(self) -> '_1423.LinearFlexibility':
        '''LinearFlexibility: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1423.LinearFlexibility.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearFlexibility. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_stiffness(self) -> '_1424.LinearStiffness':
        '''LinearStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1424.LinearStiffness.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearStiffness. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass(self) -> '_1425.Mass':
        '''Mass: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1425.Mass.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Mass. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_length(self) -> '_1426.MassPerUnitLength':
        '''MassPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1426.MassPerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_time(self) -> '_1427.MassPerUnitTime':
        '''MassPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1427.MassPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia(self) -> '_1428.MomentOfInertia':
        '''MomentOfInertia: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1428.MomentOfInertia.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertia. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1429.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1429.MomentOfInertiaPerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_per_unit_pressure(self) -> '_1430.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1430.MomentPerUnitPressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentPerUnitPressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_number(self) -> '_1431.Number':
        '''Number: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1431.Number.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Number. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_percentage(self) -> '_1432.Percentage':
        '''Percentage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1432.Percentage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Percentage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power(self) -> '_1433.Power':
        '''Power: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1433.Power.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Power. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_per_small_area(self) -> '_1434.PowerPerSmallArea':
        '''PowerPerSmallArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1434.PowerPerSmallArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerSmallArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_per_unit_time(self) -> '_1435.PowerPerUnitTime':
        '''PowerPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1435.PowerPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small(self) -> '_1436.PowerSmall':
        '''PowerSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1436.PowerSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_area(self) -> '_1437.PowerSmallPerArea':
        '''PowerSmallPerArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1437.PowerSmallPerArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1438.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1438.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_time(self) -> '_1439.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1439.PowerSmallPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure(self) -> '_1440.Pressure':
        '''Pressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1440.Pressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Pressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_per_unit_time(self) -> '_1441.PressurePerUnitTime':
        '''PressurePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1441.PressurePerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressurePerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_velocity_product(self) -> '_1442.PressureVelocityProduct':
        '''PressureVelocityProduct: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1442.PressureVelocityProduct.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureVelocityProduct. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_viscosity_coefficient(self) -> '_1443.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1443.PressureViscosityCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureViscosityCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_price(self) -> '_1444.Price':
        '''Price: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1444.Price.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Price. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_quadratic_angular_damping(self) -> '_1445.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1445.QuadraticAngularDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticAngularDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_quadratic_drag(self) -> '_1446.QuadraticDrag':
        '''QuadraticDrag: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1446.QuadraticDrag.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticDrag. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_rescaled_measurement(self) -> '_1447.RescaledMeasurement':
        '''RescaledMeasurement: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1447.RescaledMeasurement.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to RescaledMeasurement. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_rotatum(self) -> '_1448.Rotatum':
        '''Rotatum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1448.Rotatum.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Rotatum. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_safety_factor(self) -> '_1449.SafetyFactor':
        '''SafetyFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1449.SafetyFactor.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SafetyFactor. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_specific_acoustic_impedance(self) -> '_1450.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1450.SpecificAcousticImpedance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificAcousticImpedance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_specific_heat(self) -> '_1451.SpecificHeat':
        '''SpecificHeat: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1451.SpecificHeat.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificHeat. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1452.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1452.SquareRootOfUnitForcePerUnitArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_stiffness_per_unit_face_width(self) -> '_1453.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1453.StiffnessPerUnitFaceWidth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_stress(self) -> '_1454.Stress':
        '''Stress: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1454.Stress.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Stress. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature(self) -> '_1455.Temperature':
        '''Temperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1455.Temperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Temperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature_difference(self) -> '_1456.TemperatureDifference':
        '''TemperatureDifference: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1456.TemperatureDifference.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperatureDifference. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature_per_unit_time(self) -> '_1457.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1457.TemperaturePerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperaturePerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_text(self) -> '_1458.Text':
        '''Text: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1458.Text.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Text. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermal_contact_coefficient(self) -> '_1459.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1459.ThermalContactCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalContactCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermal_expansion_coefficient(self) -> '_1460.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1460.ThermalExpansionCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalExpansionCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermo_elastic_factor(self) -> '_1461.ThermoElasticFactor':
        '''ThermoElasticFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1461.ThermoElasticFactor.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermoElasticFactor. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time(self) -> '_1462.Time':
        '''Time: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1462.Time.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Time. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time_short(self) -> '_1463.TimeShort':
        '''TimeShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1463.TimeShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time_very_short(self) -> '_1464.TimeVeryShort':
        '''TimeVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1464.TimeVeryShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeVeryShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque(self) -> '_1465.Torque':
        '''Torque: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1465.Torque.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Torque. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_converter_inverse_k(self) -> '_1466.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1466.TorqueConverterInverseK.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterInverseK. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_converter_k(self) -> '_1467.TorqueConverterK':
        '''TorqueConverterK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1467.TorqueConverterK.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterK. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_per_unit_temperature(self) -> '_1468.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1468.TorquePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorquePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_velocity(self) -> '_1469.Velocity':
        '''Velocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1469.Velocity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Velocity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_velocity_small(self) -> '_1470.VelocitySmall':
        '''VelocitySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1470.VelocitySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to VelocitySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_viscosity(self) -> '_1471.Viscosity':
        '''Viscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1471.Viscosity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Viscosity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_voltage(self) -> '_1472.Voltage':
        '''Voltage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1472.Voltage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Voltage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_volume(self) -> '_1473.Volume':
        '''Volume: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1473.Volume.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Volume. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_wear_coefficient(self) -> '_1474.WearCoefficient':
        '''WearCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1474.WearCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to WearCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_yank(self) -> '_1475.Yank':
        '''Yank: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1475.Yank.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Yank. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    def default_to_metric(self):
        ''' 'DefaultToMetric' is the original name of this method.'''

        self.wrapped.DefaultToMetric()

    def default_to_imperial(self):
        ''' 'DefaultToImperial' is the original name of this method.'''

        self.wrapped.DefaultToImperial()
