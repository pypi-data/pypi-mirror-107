"""
Author:     LanHao
Date:       2021/5/31 10:11
Python:     python3.6

"""
import logging
from unittest import TestCase

logger = logging.getLogger(__name__)


class CopyTest(TestCase):
    def test_a(self):
        try:
            import ifcopenshell
            from ifcopenshell.file import file as IfcFile
        except Exception as e:
            raise Exception(f"本地IFCopenshell 环境未准备好:{e}")
        else:
            ifc_file = ifcopenshell.open("test.ifc")
            root_ins = ifc_file.by_type("ifcroot")[0]
            from copyifc.copyifc import IDCache
            ifc_new = IfcFile()
            combina = IDCache(ifc_new)
            combina.recursion_copy(root_ins)
