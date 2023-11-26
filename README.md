# lib-not-dr

A python lib came from [Difficult Rocket](https://github.com/shenjackyuanjie/Difficult-Rocket) development

一个在 [Difficult Rocket](https://github.com/shenjackyuanjie/Difficult-Rocket) 开发中 分离出来的 python 库

## Information/信息

- Version / 版本: 0.2.1
- Author / 作者: shenjackyuanjie <3695888@qq.com>

> [shenjackyuanjie](https://github.com/shenjackyuanjie)

> [更新日志|Change Log](docs/change_log.md)

### License/许可证

[MPL-2.0](https://www.mozilla.org/en-US/MPL/2.0/)

## 安装/Install

```bash title="install.sh"
pip install lib-not-dr
pip install lib-not-dr[nuitka]
# install with nuitka support
```

## 使用/Usage

### Logger

> WIP
> 等待 0.3.0

```python title="logger.py"
from lib_not_dr.logger.logger import Logger

logger = Logger.get_logger_by_name("test")

logger.fine('Hello World!')
logger.debug('Hello World!')
logger.trace('Hello tracing!')
logger.info('Hello World!')  # info!
logger.warn('warnnnnnnn')
logger.error('Hello World!')
logger.fatal('good bye world')

# tag
logger.info('this message if from tag', tag='test')
logger.debug('this debug log if from admin', tag='admin')

# end
logger.debug('and this message ends with none', end=' ')
logger.trace('so this message will be in the same line', tag='same line!')
```

### Nuitka pyproject paser

> `pyproject.toml` 内的配置
> 
> Config in `pyproject.toml`

```toml title="pyproject.toml"
[tool.lndl.nuitka]
main = "main.py"
# --main=main.py
standalone = true
onefile = false
```

> 通过 `lndl_nuitka` 命令行工具使用
> 
> Use with `lndl_nuitka` command line tool

```bash
lndl_nuitka .
lndl_nuitka . -- --onefile
# add --onefile to nuitka
lndl_nuitka . -y
# run without confirmation
lndl_nuitka . -n
# do not run
``` 

> 通过 `lib_not_dr.nuitka.reader` 模块使用
> 
> Use with `lib_not_dr.nuitka.reader`

```python
from tomli import loads
from lib_not_dr.nuitka.reader import main, run_nuitka

pyproject_toml = loads(open("pyproject.toml", "r").read())
nuitka_config = pyproject_toml["tool"]["lndl"]["nuitka"]
nuitka_config["product_version"] = "0.1.0"
command = main(nuitka_config)
run_nuitka(command)
```

### Nuitka Compiler Helper

#### Warning/警告

::: warning

> 已经弃用 Deprecated
> 请改用 lndl_nuitka / python -m lndl_nuitka

:::

> simple example
> 简单示例

```python title="simple_nuitka.py"
import subprocess
from pathlib import Path
from lib_not_dr.nuitka.compile import CompilerHelper

compiler = CompilerHelper(src_file = Path("main.py"))

print(compiler)
subprocess.run(compiler.gen_subprocess_cmd())
```

> more complex example
> 复杂示例

```python title="complex_nuitka.py"
import sys
import subprocess
from pathlib import Path
from lib_not_dr.nuitka.compile import CompilerHelper

compiler = CompilerHelper(src_file = Path("main.py"), run_after_build=True)

print(compiler)

if '-y' in sys.argv or '--yes' in sys.argv:
    do_run = True
elif '-n' in sys.argv or '--no' in sys.argv:
    do_run = False
else: # do_run is None
    while (do_run := input("compile? [y/n]").lower()) not in ["y", "n", "yes", "no"]:
        pass
        # 获取用户输入是否编译
        # get user confirmation to compile or not
    do_run = True if do_run[0] == "y" else False

if do_run:
    subprocess.run(compiler.gen_subprocess_cmd())
```
