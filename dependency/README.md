# 目录

* [path](#path)
* [json](#json)
* [png](#png)
* [audio](#audio)
* [init文件](#init)

# path

[文件跳转](_path.py)

    主要用来定义路径
    用的时候需要改点东西
    同时也定义了logging

# json

[文件跳转](_json.py)

    从path提取已定义的log
    同时定义了一个类
    类方法只有json的load&dump

## init

    file_path: 基于当前工作目录的存放目录,可以改成绝对路径
    encoding: 文件编码方式
    indent: 缩进
    ensure_ascii: 转为ascii字符

## load&dump

    根据self的参进行提取
    需要文件名和基于self.file_path文件目录的路径
    dump的第一个参是需要写入的东西,限制跟原json一致

## 示例

```python3
from ._json import Json

json = Json()
json.load('file_name', ['a', 'b', 'c'])
json.dump('dump value', 'file_name', ['a', 'b', 'c'])
```

# png

[文件跳转](_png.py)

# audio

[文件跳转](_audio.py)

# init

[文件跳转](__init__.py)
