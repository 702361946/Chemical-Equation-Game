#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import os

from chemax import Molecule

from dependency import *


def load_mods() -> tuple[dict, dict, dict, dict, dict]:
    """
    加载mods
    :return:
    """
    _user_input = input("输入mod名称:")
    _mod_path = os.path.join(os.path.join("json", "mods"), _user_input)
    if os.path.exists(_mod_path):
        _mod_config = json.load("config", ["mods", _user_input])
        _compound = json.load("compound", ["mods", _user_input])
        _condition = json.load("condition", ["mods", _user_input])
        _device = json.load("device", ["mods", _user_input])
        _element = json.load("element", ["mods", _user_input])
        if _compound is None:
            _compound = {}
        if _condition is None:
            _condition = {}
        if _device is None:
            _device = {}
        if _element is None:
            _element = {}
        return _mod_config, _compound, _condition, _device, _element
    else:
        print("mod不存在")
        return {}, {}, {}, {}, {}


def structure() -> dict:
    """
    构造mod基础结构
    :return:
    """
    _mod_config = {
        "mod_name": input("请输入mod名称:"),
        "version": "V0.1",
        "author": input("请输入作者email:"),
        "open": True,
        "description": input("请输入mod描述:"),
        "file_all": {
            "compound": False,
            "condistion": False,
            "device": False,
            "element": False,
            "README": True
        }
    }

    # 目录补全
    mod_path = os.path.join(os.path.join("json", "mods"), _mod_config["mod_name"])
    os.makedirs(mod_path, exist_ok=True)

    with open(
            os.path.join(mod_path, "README.md"),
            "w",
            encoding="UTF-8"
    ) as f:
        f.write(_mod_config["description"])

    for _i in ["compound", "condition", "device", "element"]:
        _user_input = input(f"是否加入{_i}\ny/n(默认n)")
        if _user_input == "y" or _user_input == "Y":
            _mod_config["file_all"][_i] = True
            json.dump(_mod_config, _i, ["mods", _mod_config["mod_name"]])

    json.dump(_mod_config, "config", ["mods", _mod_config["mod_name"]])
    print("mod结构已创建完成")
    return _mod_config


def add_compound(_mod_config, _compound) -> tuple[dict, dict]:
    """
    此用于添加化合物
    """
    input_compound = input("请输入化合物")
    try:
        _t = Molecule.simple_generate(input_compound).atoms

        _user_input = input("是否添加此化合物\ny/n(默认n)")
        if _user_input == "y" or _user_input == "Y":
            _compound[input_compound] = {
                "Chinese": input("请输入中文名称"),
                "make": _t,
                "buy": float(input("请输入购买价格")),
                "Discovered": input("初始是否发现(T/F)")
            }

            if _compound[input_compound]["Discovered"] == "T":
                _compound[input_compound]["Discovered"] = True
            else:
                _compound[input_compound]["Discovered"] = False

            if _mod_config["file_all"]["compound"] is False:
                _mod_config["file_all"]["compound"] = True

            print("化合物添加成功")

    except Exception as e:
        print(f"{e}\n化合物添加失败\n请输入正确的表达式")

    return _mod_config, _compound


if __name__ == '__main__':
    in_mod = False
    while True:
        print(
            "0.加载mod\n"
            "1.构造mod基础结构\n"
            "2.添加化合物\n"
            "3.添加条件\n"
            "4.添加设备\n"
            "5.修改元素\n"
            "6.保存修改\n"
            "7.退出"
        )
        user_input = input()
        if (
            in_mod is False and
            user_input != "0" and
            user_input != "1" and
            user_input != "7"
        ):
            print("请先加载或构造mod")
            continue

        match user_input:
            case "0":
                mod_config, compound, condition, device, element = load_mods()
                in_mod = True
            case "1":
                mod_config = structure()
                in_mod = True
            case "2":
                mod_config, compound = add_compound(mod_config, compound)
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6":
                json.dump(mod_config, "config", ["mods", mod_config["mod_name"]])
                json.dump(compound, "compound", ["mods", mod_config["mod_name"]])
                json.dump(condition, "condition", ["mods", mod_config["mod_name"]])
                json.dump(device, "device", ["mods", mod_config["mod_name"]])
                json.dump(element, "element", ["mods", mod_config["mod_name"]])
                print("修改已保存")
            case "7":
                exit()
            case _:
                print("未知输入")
