#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)

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


logging.info('game ok and exit')
logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
