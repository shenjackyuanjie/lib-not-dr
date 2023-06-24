# lib-not-dr

A python lib came from [Difficult Rocket](https://github.com/shenjackyuanjie/Difficult-Rocket) development

一个在 [Difficult Rocket](https://github.com/shenjackyuanjie/Difficult-Rocket) 开发中 分离出来的 python 库

## Information/信息

- Version/版本: 0.0.3

### Author/作者

[shenjackyuanjie](https://github/shenjackyuanjie)

### License/许可证

[MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/)

## 安装/Install

```bash
pip install lib-not-dr
```

## 使用/Usage

### Nuitka Compiler Helper

```python
import subprocess
from lib_not_dr.nuitka import CompilerHelper

compiler = CompilerHelper("main.py")

print(compiler)
subprocess.run(compiler.gen_subprocess_cmd())
```
