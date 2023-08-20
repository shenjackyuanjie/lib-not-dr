# Change log / 更新日志

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
