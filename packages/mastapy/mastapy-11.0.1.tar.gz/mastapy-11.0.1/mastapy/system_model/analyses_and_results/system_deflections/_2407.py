'''_2407.py

CycloidalDiscSystemDeflection
'''


from mastapy.system_model.part_model.cycloidal import _2245
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6503
from mastapy.system_model.analyses_and_results.power_flows import _3743
from mastapy.system_model.analyses_and_results.system_deflections import _2361
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CycloidalDiscSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscSystemDeflection',)


class CycloidalDiscSystemDeflection(_2361.AbstractShaftSystemDeflection):
    '''CycloidalDiscSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2245.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2245.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6503.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6503.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3743.CycloidalDiscPowerFlow':
        '''CycloidalDiscPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3743.CycloidalDiscPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
