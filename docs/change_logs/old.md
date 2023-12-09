# lndl 老版本的更新日志

## 0.2.3

### lndl-nuitka

- 现在如果没有找到 toml 解析器
  - 提示安装库 的信息里不再带有 `tomllib` 了
    - 标准库也想装 ? 🤣

## 0.2.2

### Logger

- `MainFormatter`
  - `_trace_format`
    - 通过不需要获取绝对路径时直接使用获取到的路径减少用时
- `LogMessage`
  - 不再继承 `Options`
    - `Options` 的初始化太慢了
- 终于是开始扣时间了
- `ConfigStorage`
  - 完善了功能 (虽然还是 WIP)

## 0.2.1

> logger 继续后延

### Fix

- `Logger`
  - `MainFormatter`
    - 修复了会导致 `ColorFormatter` 崩溃的问题

## 0.2.0

> 内容和 0.2.0-rc.10 相同

## 0.2.0-rc.10

### lndl-nuitka

- 将 `lndl-nuitka` 中的 `subprocess.run` 方法修改为
  - Linux / MacOS: `subprocess.run(shell=False)`
  - Windows: `subprocess.run(shell=True)`

## 0.2.0-rc.9

### lndl-nuitka

- 将运行方法修改为 `subprocess.run(shell=False)`

## 0.2.0-rc.4

### lndl-nuitka

- 在 `lndl-nuitka` 中使用新添加的 `subprocess_to_bash` 函数展示命令
  - 保证展示的命令可以直接运行

> 真的就是在刷版本号啊

## 0.2.0-rc.3

### lndl-nuitka

- 在 `arg_parser` 中添加了函数 `subprocess_to_bash`
  - 用于将 `arg_parser` 中的参数转换为 `bash` 命令
  - 理论上可以直接运行

## 0.2.0-rc.1/2

### lndl-nuitka

- 修复了一些细节问题 (反正我懒得统计具体内容了)
  - 现在不会在没有给定附加参数的时候报 `invalid args:` 了
  - 似乎没有别的细节了？

## 0.2.0-beta.2

### lndl-nuitka

- 可以使用 `--` 单独添加参数了
  - 例如 `lndl-nuitka -- --onefile`
  - 会将 `--onefile` 添加到 `nuitka` 的参数中

## 0.2.0-beta.0/1

### 重构

- 重构了文件目录结构
  - 保证 `setuptools` 可以正常工作

### lndl-nuitka

- 添加了脚本 `lndl-nuitka`
  - 用于解析 `pyproject.toml` 中的 `tool.lndl.nuitka` 部分

## 0.2.0-alpha0

### Logger

- 添加了 Logger (虽说 0.1.8 就有了)
- 目前入口点位于 `lib_not_dr.logger.logger.Logger`

## 0.1.8

- 为 `types.Options` 添加了 `_check_option` 选项
  - 为 `True` 时 会检查参数是否合法 (在类属性中已经定义了)

### Logger

- WIP (wait for 0.2.0)

## 0.1.7

- 修复了 `CompilerHelper` 中的问题
  - 重复添加 `--output-dir` 参数
- 参数喜加 2
  - `--onefile`
  - `--onefile-tempdir-spec`

## 0.1.6

- 优化了 `CompilerHelper` 的一些周围实现
  - 参数喜加一
  - `--report`

## 0.1.5

- 修复了 `types.Options` 中的 `as_markdown` 实现细节
  - 现在不会长度溢出了

## 0.1.4

- 更改了 `types.Options` 中的 `as_markdown` 实现方式
  - 原来的实现会导致 如果终端长度 > 所需长度 时, 循环一直进行
  - 同时现在分配长度是均分

## 0.1.3

- 修改了 `README.md` 内的版本号

## 0.1.2

- 改进了 `types.Options`
  - 现在 `as_markdown` 如果没有指定最长长度 会自动适配输出所用终端的宽度
  - 同时如果指定最大长度, 也会更灵活的适配
  - 补全了一些文档

## 0.1.1

- 为 `CompilerHelper` 添加了 `remove_output` 的选项
  - 用于删除编译后的过程文件

## 0.1.0

- 添加了一些文档
- `CompilerHelper`
  - 添加了 `run_after_build` 参数
    - 用于在编译完成后执行程序
  - 添加了 `compat_nuitka_version` 参数
    - 用于验证 nuitka 版本是否兼容

## 0.0.4

添加了项目的 url

## 0.0.3

继续添加了一些文档

## 0.0.2

添加了一些文档

## 0.0.1

- 添加了
  - `nuitka.compile`
    - `CompilerHelper`
  - `types.options`
    - `Options`
  - `types.version`
    - `Version`
