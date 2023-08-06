'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1150 import ElementPropertyClass
    from ._1151 import MaterialPropertyClass
