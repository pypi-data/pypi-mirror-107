'''_5121.py

MeasurementComponentMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2141
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6569
from mastapy.system_model.analyses_and_results.mbd_analyses import _5172
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MeasurementComponentMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentMultibodyDynamicsAnalysis',)


class MeasurementComponentMultibodyDynamicsAnalysis(_5172.VirtualComponentMultibodyDynamicsAnalysis):
    '''MeasurementComponentMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2141.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6569.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6569.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
