'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2287 import ActiveFESubstructureSelection
    from ._2288 import ActiveFESubstructureSelectionGroup
    from ._2289 import ActiveShaftDesignSelection
    from ._2290 import ActiveShaftDesignSelectionGroup
    from ._2291 import BearingDetailConfiguration
    from ._2292 import BearingDetailSelection
    from ._2293 import PartDetailConfiguration
    from ._2294 import PartDetailSelection
