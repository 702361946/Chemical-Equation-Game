#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import copy
import re

from config import *

if True:
    # 修改root logger的名称
    root_logger.name = 'game'
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def shop() -> None:
    logging.info("shop")
    shop_mode = "none"
    shop_all_mode = {"none", "return", "element", "compound", "device"}

    print("商店")

    # 状态判断
    def mode_if() -> bool:
        """
        当状态未知报错并退出
        当状态为return时返回False
        其他均返回True
        :return:
        """
        if shop_mode not in shop_all_mode:
            logging.error(f"Unknown shop_mode status:{shop_mode}")
            sys_exit(f"ERROR:未知状态\\{shop_mode}")
            return False
        elif shop_mode == "return":
            logging.info("return shop")
            return False
        else:
            return True

    # 购买询问
    def buy_input() -> tuple[str, list]:
        input_dict = {
            "0": {
                "describe": "购买元素",
                "transform": "element"
            },
            "1": {
                "describe": "购买化合物",
                "transform": "compound"
            },
            "2": {
                "describe": "购买仪器",
                "transform": "device"
            },
            "9": {
                "describe": "退出商店",
                "transform": "return"
            },
        }
        _shop_all_key = []

        for __i in input_dict.keys():
            print(f"{__i}.{input_dict[__i]['describe']}")

        while True:
            __t = input_dict.get(input("输入编号"), {"transform": None})["transform"]
            if __t in shop_all_mode and __t in game_values.keys():
                logging.info(f"user_input transform:{__t}")

                for __i in game_values[__t]:
                    if game_values[__t][__i]["buy"] is not False:
                        _shop_all_key.append(__i)

                if not _shop_all_key:
                    print("此选项内无可购买内容")
                    logging.info("shop_all_key None value")
                else:
                    return __t, _shop_all_key
            elif __t == "return":
                return __t, _shop_all_key
            else:
                print("无效输入")

    # 购买获取
    def buy_get(shop_all_key) -> str | None:
        get = True
        while_print = True
        while True:
            if len(shop_all_key) > 50 and get is True:
                print(
                    "可购买物过多\n"
                    "请输入包含的关键字以搜索内容\n"
                    "越准确越好\n"
                    "输入exit可退出搜索并进行下一步"
                )
                keyword = input("请输入:")
                if keyword == "exit":
                    get = False
                    continue
                filtered_items = [item for item in shop_all_key if keyword in item]

                if not filtered_items:
                    print("未找到包含该关键字的物品")
                    continue
                elif len(filtered_items) > 50:
                    print("搜索结果过多,请提供更为准确的关键字")
                    continue
                else:
                    shop_all_key = filtered_items

            _t = 0
            while _t < len(shop_all_key) and while_print is True:
                print(f"{_t}.{shop_all_key[_t]}")
                _t += 1
            while_print = False

            __t = input("请输入编号\n输入exit退出购买")
            if __t == "exit":
                return None
            try:
                __t = int(__t)
                if 0 <= __t < len(shop_all_key):
                    return shop_all_key[__t]
                else:
                    print("编号超出范围")
            except ValueError:
                print("请输入有效的数字编号")

    # 购买(我也不知道这玩意到底会不会返回None,反正报提示了)
    def buy() -> str | None:
        print(f"当前单价:{game_values[shop_mode][shop_get]['buy']}")
        while True:
            __t = input("输入购买数量(直接敲回车等同于输入1)\n输入no取消购买\n输入exit退出购买")
            if __t == "no":
                return "none"
            elif __t == "exit":
                return "return"
            elif __t == "":
                __t = 1
            else:
                try:
                    __t = int(__t)
                    if __t <= 0:
                        print("请输入大于0的数字")
                        continue
                except ValueError:
                    print("请输入有效的数字")
                    continue

            if game_values[shop_mode][shop_get]["buy"] * __t > player["money"]:
                print("余额不足")
                continue
            else:
                player["money"] -= game_values[shop_mode][shop_get]["buy"] * __t
                if shop_get not in player[shop_mode].keys():
                    player[shop_mode][shop_get] = {"value": 0}
                player[shop_mode][shop_get]["value"] += __t
                print(f"成功购买{__t}个{shop_get}")
                logging.info(f"buy:{shop_get}\\int:{__t}")
                return "none"

    while True:
        shop_mode, shop_all_key = buy_input()
        shop_all_key: list[str]

        if not mode_if():
            return None

        shop_get = buy_get(shop_all_key)
        if shop_get is None:
            return None

        shop_mode = buy()
        if not mode_if():
            return None


def equation():
    logging.info("equation")

    equation_all_key = {
        "reactants": {},
        "product": {},
        "all": {}
    }

    _user_input = input("请输入化学方程式\n格式要求如下\na+b+c=d\n加号及等号间无空格\n")
    logging.debug(f"user_input:{_user_input}")
    _user_input = _user_input.split("=")
    if len(_user_input) != 2:
        print("请输入正确的化学方程式")
        return False

    equation_mode = "reactants"

    for _i in _user_input:
        for __i in _i.split("+"):
            num = re.match(r"^\d+", __i)
            key = __i[num.end():] if num is not None else __i
            num = int(num.group()) if num else 1
            equation_all_key[equation_mode][key] = num

        equation_mode = "product"

    for _i in equation_all_key["reactants"].keys():
        if _i not in element.keys() and _i not in compound.keys():
            print(f'元素"{_i}"不存在\n如果真实存在请联系702361946@qq.com')
            equation_mode = "return"

    if equation_mode == "return":
        return False

    for _i in equation_all_key["product"].keys():
        if _i in compound.keys():
            for __i in compound[_i]["make"].keys():
                if __i not in equation_all_key["all"].keys():
                    equation_all_key["all"][__i] = 0
                equation_all_key["all"][__i] += (
                        compound[_i]["make"][__i] * equation_all_key["product"][_i]
                )
        else:
            if _i not in equation_all_key["all"].keys():
                equation_all_key["all"][_i] = 0
            equation_all_key["all"][_i] += equation_all_key["product"][_i]

    equation_all_reactants = copy.deepcopy(equation_all_key["all"])

    for _i in equation_all_key["reactants"].keys():
        if _i in compound.keys():
            for __i in compound[_i]["make"].keys():
                if __i not in equation_all_reactants.keys():
                    equation_all_reactants[__i] = 0
                equation_all_reactants[__i] -= (
                    compound[_i]["make"][__i] *
                    equation_all_key["reactants"][_i]
                )
        else:
            if _i not in equation_all_reactants.keys():
                equation_all_reactants[_i] = 0
            equation_all_reactants[_i] -= equation_all_key["reactants"][_i]

    logging.debug(f"equation_all_key\n{equation_all_key}")

    for _i in equation_all_reactants.keys():
        if equation_all_reactants[_i] != 0:
            print(f"方程式未配平\n{_i}:{equation_all_reactants[_i]}")
            equation_mode = "return"
        elif (
                equation_all_key["all"][_i] >
                player["compound"].get(_i, {"value": 0})["value"] and
                equation_all_key["all"][_i] >
                player["element"].get(_i, {"value": 0})["value"]
        ):
            print(f"当前持有的化合物不足以支撑反应:{_i}")
            equation_mode = "return"

    if equation_mode == "return":
        return False

    for _i in equation_all_key["all"].keys():
        if _i in compound.keys():
            if _i not in player["compound"].keys():
                player["compound"][_i] = {
                    "value": 0
                }
            player["compound"][_i]["value"] -= equation_all_key["all"][_i]
        else:
            if _i not in player["element"].keys():
                player["element"][_i] = {
                    "value": 0
                }
            player["element"][_i]["value"] -= equation_all_key["all"][_i]

    for _i in equation_all_key["product"].keys():
        if _i in compound.keys():
            if _i not in player["compound"].keys():
                player["compound"][_i] = {
                    "value": 0
                }
            player["compound"][_i]["value"] += equation_all_key["product"][_i]
        else:
            if _i not in player["element"].keys():
                player["element"][_i] = {
                    "value": 0
                }
            player["element"][_i]["value"] += equation_all_key["product"][_i]

    json.dump(player, "player")
    return True


def order_page():
    logging.info("order")

    while len(order) < 5:
        add_order()
    json.dump(order, "order")

    _t = 0
    order_all_list = list(order.keys())
    for _i in order_all_list:
        print(f"id:{_t}")
        for __i in order[_i]["get"].keys():
            print(f"需要:{__i}x{order[_i]['get'][__i]['get']}")
            print(f"已交付:{__i}x{order[_i]['get'][__i]['user_get']}")
        print(f"完成可得报酬:{order[_i]['money']}\n")
        _t += 1

    while True:
        _user_input = input("请输入订单编号\nexit 退出订单页")
        if _user_input == "exit":
            return None
        elif (
            _user_input.isdigit() and
            int(_user_input) in range(len(order_all_list))
        ):
            order_id = order_all_list[int(_user_input)]
            break
        else:
            print("未知内容")

    order_all_value = {}
    for _i in order[order_id]["get"].keys():
        if (
            order[order_id]["get"][_i]["user_get"] >=
            order[order_id]["get"][_i]["get"]
        ):
            continue
        order_all_value[_i] = {
            "end": (
                order[order_id]["get"][_i]['get'] -
                order[order_id]["get"][_i]['user_get']
            ),
        }

    for _i in order_all_value.keys():
        print(f"{_i}还差{order_all_value[_i]['end']}")

    while True:
        _user_input = input("请输入需要交付的元素\nexit 退出订单页")
        if _user_input == "exit":
            return None
        elif _user_input in order_all_value.keys():
            if _user_input in player["element"].keys():
                _mode = "element"
            elif _user_input in player["compound"].keys():
                _mode = "compound"
            else:
                print(f"仓库里暂无存货:{_user_input}")
                continue

            _get = _user_input

            print(f"仓库内还有{player[_mode][_get]['value']}个")
            _user_input = input("请输入需要交付的数量")
            if _user_input.isdigit():
                _user_input = int(_user_input)
            else:
                print("请输入整数")
                continue
            if _user_input > player[_mode][_get]["value"]:
                print("数量不足")
                get_bool = False
            elif _user_input >= order_all_value[_get]["end"]:
                order[order_id]["get"][_get]["user_get"] += (
                    order_all_value[_get]["end"]
                )
                player[_mode][_get]["value"] -= order_all_value[_get]["end"]
                order_all_value[_get]["end"] = 0
                get_bool = True
            else:
                order[order_id]["get"][_get]["user_get"] += _user_input
                order_all_value[_get]["end"] -= _user_input
                player[_mode][_get]["value"] -= _user_input
                get_bool = True
            if get_bool:
                print("成功提交")

                del_order = True
                _return = False
                for _i in order[order_id]["get"].keys():
                    if (
                        order[order_id]["get"][_i]["user_get"] <
                        order[order_id]["get"][_i]["get"]
                    ):
                        del_order = False
                        break
                if del_order:
                    print("订单完成")
                    player["money"] += order[order_id]["money"]
                    print(f"获得报酬:{order[order_id]['money']}")
                    del order[order_id]
                    _return = True
                    json.dump(player, "player")

                json.dump(order, "order")
                if _return:
                    return True

        else:
            print("未知内容")


def main():
    logging.info("main")
    while True:
        print("主菜单")
        _user_input = input("0.商店\n1.合成\n2.订单\n9.退出")
        match _user_input:
            case "0":
                shop()
            case "1":
                equation()
            case "2":
                order_page()
            case "9":
                json.dump(player, "player")
                logging.info("user in main page exit")
                sys_exit()
            case _:
                print("未知输入")


if __name__ == '__main__':
    main()

logging.info('game ok and exit')
logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
