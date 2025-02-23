# 游戏简介

    这是一款基于python且关于化学方程式的游戏,
    玩家需要通过不断的通过购买元素&化合物,
    以合成出更多新的化合物,
    并通过订单的方式获得奖励.
    不断重复

# 源码环境

## 编译器

    python312+

## 依赖

    dependency下的所有内容(虽然确实有点少)

# 项目架构

## dependency

    依赖库

## json

    任何json文件的存放处

## .\

    源码编写区

### config.py

    一切基础全局参&文件校验等

### game.py

    游戏内部逻辑函数,内含游戏循环,可通过覆写实现自定义内容

# mods

## 架构
    .\json\player.json下的key"open_mod"将决定是否启用所有mod
    此值默认为true

    .\json\modes\mod名\*.json
    需要1+5个文件
    config.json(必须)

    compound.json
    condistion.json
    device.json
    element.json
    README.md(用以自述)

## config格式

    {
        "mod_name": "mod名",
        "version": "mod版本",
        "author": "mod作者(最好是邮箱)",
        "open": true | false,(用以标识是否启用整个mod)
        "description": "mod描述",
        "file_all": {
            "compound": true | false,
            "condistion": true | false,
            "device": true | false,
            "element": true | false,(只可修改价格)
            "README": true | false
            须知: t|f用以标识是否启用(README为是否存在)
        }
    }

## json

    目前mods仅支持以json文件形式,
    文件内字典的key-value请参考同名文件

## mod所有权

    mod的所有权均由mod作者所持有
    mod作者可自行转让所有权
    可自行决定是否收费(max: 50CNY)

# 存在的问题

    dict KeyError问题
    暂未覆盖常见化合物
    无法确认化学方程式是否合法
    无法保证玩家是否有能力完成订单内容
    无法对化学方程式添加附加条件(如催化剂等)
    代码逻辑可能存在问题
    代码未优化
    
    重要！
    无UI界面

# 下一个版本目标

## 必须

    优化目前代码
    添加更多常见化合物

## 可能

    实现化学式合法检查
    生成玩家有能力完成的订单
    实现探索功能(买设备做实验?)
    ...

    
    