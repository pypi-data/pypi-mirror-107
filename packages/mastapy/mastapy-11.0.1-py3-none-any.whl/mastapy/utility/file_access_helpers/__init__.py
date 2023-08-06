'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1547 import ColumnTitle
    from ._1548 import TextFileDelimiterOptions
