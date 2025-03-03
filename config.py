#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import os
import random
import sys
from uuid import uuid4

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

    order = json.load("order")
    if type(order).__name__!= "dict":
        logging.info("读取order出现问题")
        print("无法获取正在进行的订单")
        order = {}

    # mods
    if player["open_mod"] is True:
        logging.info("mod开启")

        mods_dict = {}
        mods_path = ".\\json\\mods"

        if os.path.exists(mods_path):
            for mod_name in os.listdir(mods_path):
                mod_dir = os.path.join(mods_path, mod_name)
                if os.path.isdir(mod_dir):
                    _t = json.load("config", ["mods", mod_name])
                    if type(_t).__name__!= "dict":
                        print(f"获取mod失败:{mod_dir}")
                        logging.info(f"获取mod失败:{mod_dir}")
                        continue
                    logging.info(f"获取mod成功:{mod_dir}")
                    print(f"成功找到mod:{mod_name}")
                    if "open" in _t.keys() and "file_all" in _t.keys():
                        if _t["open"] is True:
                            mods_dict[mod_name] = _t
                            print(f"此mod已开启:{mod_name}")
                            logging.info(f"此mod已开启:{mod_name}")
                        else:
                            logging.info(f"此mod已关闭:{mod_name}")

            for mod_name in mods_dict.keys():
                _t = mods_dict[mod_name]
                if type(_t["file_all"]).__name__!= "dict":
                    logging.info(f"此mod配置错误:{mod_name}\n{_t}")
                    print(f"此mod配置错误:{mod_name}")
                    continue
                for mode in ["compound", "condition", "device", "element"]:
                    if _t["file_all"].get(mode, False) is not True:
                        continue

                    __t = json.load(mode, ["mods", mod_name])
                    if type(__t).__name__!= "dict":
                        logging.info(f"此mod_{mode}文件错误:{mod_name}\n{__t}")
                        continue

                    for _i in __t.keys():
                        if type(__t[_i]).__name__!= "dict":
                            logging.info(f"not dict:{mode}\n{mod_name}\n{__t[_i]}")
                            continue

                        match mode:
                            case "compound":
                                compound[_i] = __t[_i]
                            case "condition":
                                condition[_i] = __t[_i]
                            case "device":
                                if (
                                    _i not in device.keys() or
                                    "buy" in __t[_i].keys()
                                ):
                                    device[_i] = __t[_i]
                            case "element":
                                if (
                                    "buy" in __t[_i].keys() and
                                    __t[_i]["buy"] is not None
                                ):
                                    element[_i]["buy"] = __t[_i]["buy"]
                            case _:
                                logging.error(f"no mode:{mode}")

                print(f"此mod加载已完成:{mod_name}")
        else:
            logging.info("mods文件夹不存在")
            print("mods文件夹不存在")

    game_values = {
        "player": player,
        "device": device,
        "element": element,
        "compound": compound,
        "condition": condition,
        "order": order
    }


def add_order():
    _id = uuid4().hex
    get = {} # 需求
    money = 0

    all_key = {**element, **compound}

    size = min(5, len(all_key))

    all_items = random.sample(
        list(all_key.keys()),
        random.randint(1, size)
    )

    for _i in all_items:
        if _i not in get.keys():
            get[_i] = {
                "get": random.randint(1, 100),
                "user_get": 0,
            }
            money += int(
                get[_i]["get"] *
                all_key[_i]["buy"] *
                random.uniform(1.1, 2)
            )

    order[_id] = {
        "id": _id,
        "get": get,
        "money": money,
    }


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
