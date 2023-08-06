'''_3549.py

SynchroniserStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2278
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6617
from mastapy.system_model.analyses_and_results.stability_analyses import _3529
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SynchroniserStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserStabilityAnalysis',)


class SynchroniserStabilityAnalysis(_3529.SpecialisedAssemblyStabilityAnalysis):
    '''SynchroniserStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2278.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6617.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6617.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
