#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import copy
import re

from config import *

if True:
    # 修改root logger的名称
    root_logger.name = 'game'
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def shop():
    logging.info("shop")
    shop_all_key = []
    shop_mode = "none"
    while True:
        print("商店")
        _user_input = input("0.购买元素\n1.购买化合物\n2.购买仪器\n9.返回")
        match _user_input:
            case "0":
                shop_mode = "元素"
                for _i in element.keys():
                    if element[_i]["buy"] is not False:
                        shop_all_key.append(_i)

                if len(shop_all_key) == 0:
                    print("没有可购买的元素")
                    shop_mode = "none"
            case "1":
                shop_mode = "化合物"
                for _i in compound.keys():
                    if compound[_i]["buy"] is not False:
                        shop_all_key.append(_i)

                if len(shop_all_key) == 0:
                    print("没有可购买的化合物")
                    shop_mode = "none"
            case "2":
                shop_mode = "仪器"
                for _i in device.keys():
                    if device[_i]["buy"] is not False:
                        shop_all_key.append(_i)

                if len(shop_all_key) == 0:
                    print("没有可购买的仪器")
                    shop_mode = "none"
            case "9":
                json.dump(player, "player")
                return None
            case _:
                print("未知输入")

        if shop_mode != "none":
            print(f"可购买的{shop_mode}有")
            _t = 0
            while _t < len(shop_all_key):
                print(f"{_t}.{shop_all_key[_t]}")
                _t += 1

            while True:
                _user_input = input("请输入编号")
                try:
                    _user_input = int(_user_input)
                    if _user_input in range(len(shop_all_key)):
                        match shop_mode:
                            case "元素":
                                shop_buy_money = element[shop_all_key[_user_input]]["buy"]
                                shop_mode = "element"
                            case "化合物":
                                shop_buy_money = compound[shop_all_key[_user_input]]["buy"]
                                shop_mode = "compound"
                            case "仪器":
                                shop_buy_money = device[shop_all_key[_user_input]]["buy"]
                                shop_mode = "device"
                            case _:
                                logging.error(f"shop_mode value error:{shop_mode}")
                                sys_exit("请发送日志文件至702361946@qq.com")
                        if player["money"] >= shop_buy_money:
                            player["money"] -= shop_buy_money
                            if shop_all_key[_user_input] not in player[shop_mode].keys():
                                player[shop_mode][shop_all_key[_user_input]] = {
                                    "value": 0
                                }
                            player[shop_mode][shop_all_key[_user_input]]["value"] += 1
                            print(f"购买成功，剩余{player['money']}")
                            shop_all_key = []
                            shop_mode = "none"
                            logging.info(f"shop\\{shop_all_key[_user_input]}+1")
                            break
                        else:
                            print(f"余额不足，需要{shop_buy_money}")
                            shop_mode = "none"
                            continue

                    else:
                        print("请输入正确的编号")
                        continue

                except ValueError:
                    print("请输入整数")
                    continue


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


logging.info('game ok and exit')
logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
