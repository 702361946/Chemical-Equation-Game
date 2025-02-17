#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

import json
import logging
import os.path
from datetime import datetime

from ._path import root_logger

if True:
    # 修改root logger的名称
    root_logger.name = 'jsons'
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Json(object):
    def __init__(
            self,
            file_path: str = 'json',
            encoding: str = 'utf-8',
            indent: int = 4,
            ensure_ascii: bool = False
    ) -> object:
        logging.info("json\\__init__")
        if type(indent).__name__ != 'int':
            logging.error('indent type not int')
            raise TypeError('indent type not int')
        if type(ensure_ascii).__name__ != 'bool':
            logging.error('ensure_ascii type not bool')
            raise TypeError('ensure_ascii type not bool')

        self.file_path = file_path
        self.encoding = encoding
        self.indent = indent
        self.ensure_ascii = ensure_ascii

        logging.info('ok')

    def dump(self, a, file_name: str, file_path: list[str] | str = None) -> bool:
        """
        写入文件
        :param a: 要写入的内容
        :param file_name: 要写入的文件名,不带后缀
        :param file_path: 中间的文件夹,如果没有请放空,在list里填文件夹名称,顺序拼接
        :return: True&False
        """
        logging.info(f'json\\w\nfile_path{file_path}\nfile_name:{file_name}\nw:{a}')
        try:
            if type(file_path).__name__ in ['list', 'str']:
                if type(file_path).__name__ != 'list':
                    file_path = [file_path]
                __t = self.file_path
                for _t in file_path:
                    __t = os.path.join(__t, _t)
                file_path = os.path.join(__t, file_name)
            elif file_path is None:
                file_path = os.path.join(self.file_path, file_name)
            else:
                raise TypeError('file_path type is list or str')

            # 目录补全
            os.makedirs(os.path.dirname(f'{file_path}.json'), exist_ok=True)

            with open(
                    f'{file_path}.json',
                    'w+',
                    encoding=self.encoding
            ) as f:
                json.dump(a, f, indent=self.indent, ensure_ascii=self.ensure_ascii)
                logging.info('ok')
                return True
        except Exception as e:
            logging.error(e)
            return False

    def load(self, file_name: str, file_path: list[str] | str = None):
        """
        读取文件
        :param file_name: 要写入的文件名,不带后缀
        :param file_path: 中间的文件夹,如果没有请放空,在list里填文件夹名称,顺序拼接
        :return: 文件内容&False
        """
        logging.info(f'json\\r\\file_name:{file_name}')
        try:
            if type(file_path).__name__ in ['list', 'str']:
                if type(file_path).__name__ != 'list':
                    file_path = [file_path]
                __t = self.file_path
                for _t in file_path:
                    __t = os.path.join(__t, _t)
                file_path = os.path.join(__t, file_name)
            elif file_path is None:
                file_path = os.path.join(self.file_path, file_name)
            else:
                raise TypeError('file_path type is list or str')

            with open(
                    f'{file_path}.json',
                    'r+',
                    encoding=self.encoding
            ) as f:
                a = json.load(f)
                logging.info('ok')
                return a

        except Exception as e:
            logging.error(e)
            return False

    def logging_get(self) -> None:
        """
        打印到日志中
        """
        logging.info('json\\logging_get\n')
        logging.info(f'file_path:{self.file_path}')
        logging.info(f'encoding:{self.encoding}')
        logging.info(f'indent:{self.indent}')
        logging.info(f'ensure_ascii:{self.ensure_ascii}')
        logging.info('END\n')


logging.info('json ok and exit')
logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
