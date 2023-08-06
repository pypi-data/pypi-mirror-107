'''_6372.py

DatumCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2127
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6243
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6346
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'DatumCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundCriticalSpeedAnalysis',)


class DatumCompoundCriticalSpeedAnalysis(_6346.ComponentCompoundCriticalSpeedAnalysis):
    '''DatumCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2127.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2127.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6243.DatumCriticalSpeedAnalysis]':
        '''List[DatumCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6243.DatumCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6243.DatumCriticalSpeedAnalysis]':
        '''List[DatumCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6243.DatumCriticalSpeedAnalysis))
        return value
