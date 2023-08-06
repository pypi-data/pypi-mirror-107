'''_2541.py

ClutchHalfCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2255
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2381
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2557
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ClutchHalfCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundSystemDeflection',)


class ClutchHalfCompoundSystemDeflection(_2557.CouplingHalfCompoundSystemDeflection):
    '''ClutchHalfCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundSystemDeflection.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_2381.ClutchHalfSystemDeflection]':
        '''List[ClutchHalfSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2381.ClutchHalfSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2381.ClutchHalfSystemDeflection]':
        '''List[ClutchHalfSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2381.ClutchHalfSystemDeflection))
        return value
