'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1476 import ScriptingSetup
    from ._1477 import UserDefinedPropertyKey
    from ._1478 import UserSpecifiedData
