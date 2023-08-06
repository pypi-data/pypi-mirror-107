'''_3585.py

ClutchHalfCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2255
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3452
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3601
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ClutchHalfCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundStabilityAnalysis',)


class ClutchHalfCompoundStabilityAnalysis(_3601.CouplingHalfCompoundStabilityAnalysis):
    '''ClutchHalfCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2255.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2255.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3452.ClutchHalfStabilityAnalysis]':
        '''List[ClutchHalfStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3452.ClutchHalfStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3452.ClutchHalfStabilityAnalysis]':
        '''List[ClutchHalfStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3452.ClutchHalfStabilityAnalysis))
        return value
