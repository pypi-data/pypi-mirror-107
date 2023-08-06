'''_2404.py

CycloidalAssemblySystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6501
from mastapy.system_model.analyses_and_results.power_flows import _3740
from mastapy.system_model.analyses_and_results.system_deflections import _2462, _2473
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CycloidalAssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblySystemDeflection',)


class CycloidalAssemblySystemDeflection(_2473.SpecialisedAssemblySystemDeflection):
    '''CycloidalAssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2244.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6501.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6501.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3740.CycloidalAssemblyPowerFlow':
        '''CycloidalAssemblyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3740.CycloidalAssemblyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def ring_pins_to_disc_connections(self) -> 'List[_2462.RingPinsToDiscConnectionSystemDeflection]':
        '''List[RingPinsToDiscConnectionSystemDeflection]: 'RingPinsToDiscConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPinsToDiscConnections, constructor.new(_2462.RingPinsToDiscConnectionSystemDeflection))
        return value
