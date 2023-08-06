'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2023 import ClutchConnection
    from ._2024 import ClutchSocket
    from ._2025 import ConceptCouplingConnection
    from ._2026 import ConceptCouplingSocket
    from ._2027 import CouplingConnection
    from ._2028 import CouplingSocket
    from ._2029 import PartToPartShearCouplingConnection
    from ._2030 import PartToPartShearCouplingSocket
    from ._2031 import SpringDamperConnection
    from ._2032 import SpringDamperSocket
    from ._2033 import TorqueConverterConnection
    from ._2034 import TorqueConverterPumpSocket
    from ._2035 import TorqueConverterTurbineSocket
