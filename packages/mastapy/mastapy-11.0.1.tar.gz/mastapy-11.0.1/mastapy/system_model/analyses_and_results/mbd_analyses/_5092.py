'''_5092.py

FaceGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2205
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6531
from mastapy.system_model.analyses_and_results.mbd_analyses import _5091, _5090, _5098
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FaceGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetMultibodyDynamicsAnalysis',)


class FaceGearSetMultibodyDynamicsAnalysis(_5098.GearSetMultibodyDynamicsAnalysis):
    '''FaceGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2205.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2205.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6531.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6531.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5091.FaceGearMultibodyDynamicsAnalysis]':
        '''List[FaceGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5091.FaceGearMultibodyDynamicsAnalysis))
        return value

    @property
    def face_gears_multibody_dynamics_analysis(self) -> 'List[_5091.FaceGearMultibodyDynamicsAnalysis]':
        '''List[FaceGearMultibodyDynamicsAnalysis]: 'FaceGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsMultibodyDynamicsAnalysis, constructor.new(_5091.FaceGearMultibodyDynamicsAnalysis))
        return value

    @property
    def face_meshes_multibody_dynamics_analysis(self) -> 'List[_5090.FaceGearMeshMultibodyDynamicsAnalysis]':
        '''List[FaceGearMeshMultibodyDynamicsAnalysis]: 'FaceMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesMultibodyDynamicsAnalysis, constructor.new(_5090.FaceGearMeshMultibodyDynamicsAnalysis))
        return value
