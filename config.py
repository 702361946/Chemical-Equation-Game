#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

import sys

from dependency import *

if True:
    # 修改root logger的名称
    root_logger.name = 'config'
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def sys_exit(message = None):
    print(f"\n{message}\n")
    logging.info(f"exit message:{message}")
    input("按下回车以退出")
    sys.exit()


# 基本全局参
if True:
    player = json.load("player")
    device = json.load("device")
    element = json.load("element")
    compound = json.load("compound")
    condition = json.load("condition")

    if (
        type(player).__name__!= "dict" or
        type(device).__name__ != "dict" or
        type(element).__name__ != "dict" or
        type(compound).__name__ != "dict" or
        type(condition).__name__ != "dict"
    ):
        sys_exit("请检查文件完整性")

# 类型提示(如无必要勿删改)
if True:
    device: dict[str, dict[str, int]]
    """
    {
        "仪器名": {
            "buy": 价格\\False
        }
    }
    """

    condition: dict[str, dict[str, list[str]]]
    """
    {
        "条件名": {
            "available": ["可选仪器"]
        }
    }
    """

    element: dict[str, dict[str, str | int | list | bool]]
    """
    {
        "元素符号": {
            'Chinese': "中文名",
            "Valence": [化合价],
            "buy": 价格\\False,
            "Discovered": True
        }
    }
    """

    compound: dict[str, dict[str, str | int | bool | dict[str, int]]]
    """
    {
        "H2O": {
            "Chinese": "水",
            "make": {
                "H": 2,
                "O": 1
            },
            "buy": 价格\\False,
            "Discovered": True
        }
    }
    """
    player: dict[str, int | dict]
    """
    {
    "money": 100,
    "device": {},
    "element": {},
    "compound": {},
    }
    """

logging.info('config ok and exit')
logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
