'''_6373.py

ExternalCADModelCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6244
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6346
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ExternalCADModelCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundCriticalSpeedAnalysis',)


class ExternalCADModelCompoundCriticalSpeedAnalysis(_6346.ComponentCompoundCriticalSpeedAnalysis):
    '''ExternalCADModelCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6244.ExternalCADModelCriticalSpeedAnalysis]':
        '''List[ExternalCADModelCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6244.ExternalCADModelCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6244.ExternalCADModelCriticalSpeedAnalysis]':
        '''List[ExternalCADModelCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6244.ExternalCADModelCriticalSpeedAnalysis))
        return value
