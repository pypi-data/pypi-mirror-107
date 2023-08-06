'''_5176.py

WormGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6634
from mastapy.system_model.analyses_and_results.mbd_analyses import _5175, _5174, _5098
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetMultibodyDynamicsAnalysis',)


class WormGearSetMultibodyDynamicsAnalysis(_5098.GearSetMultibodyDynamicsAnalysis):
    '''WormGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2228.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6634.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6634.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5175.WormGearMultibodyDynamicsAnalysis]':
        '''List[WormGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5175.WormGearMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_gears_multibody_dynamics_analysis(self) -> 'List[_5175.WormGearMultibodyDynamicsAnalysis]':
        '''List[WormGearMultibodyDynamicsAnalysis]: 'WormGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsMultibodyDynamicsAnalysis, constructor.new(_5175.WormGearMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_meshes_multibody_dynamics_analysis(self) -> 'List[_5174.WormGearMeshMultibodyDynamicsAnalysis]':
        '''List[WormGearMeshMultibodyDynamicsAnalysis]: 'WormMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesMultibodyDynamicsAnalysis, constructor.new(_5174.WormGearMeshMultibodyDynamicsAnalysis))
        return value
