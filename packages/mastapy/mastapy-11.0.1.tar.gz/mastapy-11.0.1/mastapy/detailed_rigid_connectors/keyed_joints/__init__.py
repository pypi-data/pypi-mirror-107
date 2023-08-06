'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1202 import KeyedJointDesign
    from ._1203 import KeyTypes
    from ._1204 import KeywayJointHalfDesign
    from ._1205 import NumberOfKeys
