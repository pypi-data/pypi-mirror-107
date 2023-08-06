"""
Author:     LanHao
Date:       2021/5/31 10:09
Python:     python3.6

"""
import logging
from typing import Dict, Iterable, List

from ifcopenshell.file import file as IfcFile
from ifcopenshell.entity_instance import entity_instance

logger = logging.getLogger(__name__)


class IDCache(object):
    """

    特定的一个缓存复制类,对应一个原始文件.如果从不同的文件中复制,那么需要对应不同给的实例

    """
    _global_id_key: str = "id"
    _global_id_key_map: Dict = None
    _ifc_file: IfcFile = None

    def __init__(self, ifc_file: IfcFile):
        """
        初始化,用于记录需要往那个文件中复制.

        :param ifc_file: IfcFile
        """
        self._global_id_key_map = {}
        self._ifc_file = ifc_file

    def recursion_copy(self, ins: entity_instance) -> entity_instance:
        """
        递归的方式进行复制

        :param ins:entity_instance
        :return: entity_instance
        """

        _back = None

        if isinstance(ins, (str, int, float)):
            _back = ins
        elif isinstance(ins, entity_instance):
            # 此处为核心的处理方式,递归调用
            info: Dict = ins.get_info()
            global_id = info.get(self._global_id_key)

            if global_id and global_id in self._global_id_key_map.keys():
                _back = self._global_id_key_map[global_id]
            else:  # global_id 不存在亦或者缓存中未记录
                info.pop(self._global_id_key)

                inf_new = {}

                for key, value in info.items():
                    if isinstance(value, entity_instance):
                        value_new = self.recursion_copy(value)
                    elif isinstance(value, (str, int, float, type(None))):
                        value_new = value
                    elif isinstance(value, Iterable):
                        value_new = [self.recursion_copy(value_i) for value_i in value]
                    else:
                        raise Exception(f"遇到其他的数据对象:key:{key},{value},type:{type(value)}")

                    inf_new[key] = value_new
                try:
                    new_entity = self._ifc_file.create_entity(**inf_new)
                    self._global_id_key_map[global_id] = new_entity
                except Exception as e:
                    logger.error(f"发生错误,原始元素为:{info}")
                    raise e
                else:
                    _back = new_entity

        else:  # TODO 并不知道此处传入的对象中,除了常见的数字，字符串类型和entity_instance 外，是否还有别的类型,未做兼容处理
            raise Exception(f"预料之外的ifc 对象:{ins}")
        return _back
