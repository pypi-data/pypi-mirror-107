'''_2488.py

SynchroniserHalfSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections import _2380, _2489
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2280
from mastapy.system_model.analyses_and_results.static_loads import _6616
from mastapy.system_model.analyses_and_results.power_flows import _3813
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SynchroniserHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfSystemDeflection',)


class SynchroniserHalfSystemDeflection(_2489.SynchroniserPartSystemDeflection):
    '''SynchroniserHalfSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_connection(self) -> '_2380.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2380.ClutchConnectionSystemDeflection)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def component_design(self) -> '_2280.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2280.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6616.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6616.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3813.SynchroniserHalfPowerFlow':
        '''SynchroniserHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3813.SynchroniserHalfPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
