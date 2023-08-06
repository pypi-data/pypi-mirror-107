'''_6278.py

PointLoadCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model import _2149
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6585
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6314
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'PointLoadCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCriticalSpeedAnalysis',)


class PointLoadCriticalSpeedAnalysis(_6314.VirtualComponentCriticalSpeedAnalysis):
    '''PointLoadCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2149.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6585.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6585.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
