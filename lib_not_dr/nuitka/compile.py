#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import platform
import warnings
from pathlib import Path
from typing import List, Tuple, Optional, Union, Any

from lib_not_dr.types import Options, Version, VersionRequirement


def ensure_cmd_readable(cmd: str) -> str:
    """
    保证 参数中 不含空格
    :param cmd: 要格式化的命令行参数
    :return: 格式化后的命令行参数
    """
    if ' ' in cmd:
        return f'"{cmd}"'
    return cmd


def format_cmd(arg_name: Optional[str] = None,
               arg_value: Optional[Union[str, List[str]]] = None,
               write: Optional[Any] = True) -> List[str]:
    """
    用来格式化输出命令行参数
    :param arg_name: 类似 --show-memory 之类的主项
    :param arg_value: 类似 xxx 类的内容
    :param write: 是否写入
    :return: 直接拼接好的命令行参数 不带 =
    """
    if not write:
        return []
    if arg_name is None:
        return []
    if arg_value is None:
        return [arg_name]
    if isinstance(arg_value, list):
        arg_value = ','.join([ensure_cmd_readable(value) for value in arg_value])
        return [f'{arg_name}{arg_value}']
    arg_value = ensure_cmd_readable(arg_value)
    return [f'{arg_name}{arg_value}']


class CompilerHelper(Options):
    """
    用于帮助生成 nuitka 构建脚本的类
    Use to help generate nuitka build script
    
    """
    name = 'Nuitka Compiler Helper'

    output_path: Path = Path('./build')
    src_file: Path

    python_cmd: str = 'python'
    compat_nuitka_version: VersionRequirement = VersionRequirement("~1.7.1")  # STATIC VERSION

    # 以下为 nuitka 的参数
    # nuitka options below
    use_lto: bool = False  # --lto=yes (no is faster)
    use_clang: bool = True  # --clang
    use_msvc: bool = True  # --msvc=latest
    use_mingw: bool = False  # --mingw64
    standalone: bool = True  # --standalone
    use_ccache: bool = True  # not --disable-ccache
    enable_console: bool = True  # --enable-console / --disable-console

    show_progress: bool = True  # --show-progress
    show_memory: bool = False  # --show-memory
    remove_output: bool = True  # --remove-output
    save_xml: bool = False  # --xml
    xml_path: Path = Path('build/compile_data.xml')

    download_confirm: bool = True  # --assume-yes-for-download
    run_after_build: bool = False  # --run

    company_name: Optional[str] = ''
    product_name: Optional[str] = ''
    file_version: Optional[Version] = None
    product_version: Optional[Version] = None
    file_description: Optional[str] = ''  # --file-description

    copy_right: Optional[str] = ''  # --copyright

    icon_path: Optional[Path] = None

    follow_import: List[str] = []
    no_follow_import: List[str] = []

    include_data_dir: List[Tuple[str, str]] = []
    include_packages: List[str] = []

    enable_plugin: List[str] = []  # --enable-plugin=xxx,xxx
    disable_plugin: List[str] = []  # --disable-plugin=xxx,xxx

    def init(self, **kwargs) -> None:
        if (compat_version := kwargs.get('compat_nuitka_version')) is not None:
            if not self.compat_nuitka_version.accept(compat_version):
                warnings.warn(
                    f"Nuitka version may not compat with {compat_version}\n"
                    "requirement: {self.compat_nuitka_version}"
                )
        # 非 windows 平台不使用 msvc
        if platform.system() != 'Windows':
            self.use_msvc = False
            self.use_mingw = False
        else:
            self.use_mingw = self.use_mingw and not self.use_msvc
            # Windows 平台下使用 msvc 时不使用 mingw

    def __str__(self):
        return self.as_markdown()

    def as_markdown(self, longest: Optional[int] = None) -> str:
        """
        输出编译器帮助信息
        Output compiler help information
        
        Args:
            longest (Optional[int], optional): 
                输出信息的最大长度限制 The maximum length of output information. 
                Defaults to None.

        Returns:
            str: 以 markdown 格式输出的编译器帮助信息
                Compile helper information in markdown format
        """
        front = super().as_markdown(longest)
        gen_cmd = self.gen_subprocess_cmd()
        return f"{front}\n\n```bash\n{' '.join(gen_cmd)}\n```"

    def gen_subprocess_cmd(self) -> List[str]:
        """生成 nuitka 构建脚本
        Generate nuitka build script

        Returns:
            List[str]: 
                生成的 nuitka 构建脚本
                Generated nuitka build script
        """
        cmd_list = [self.python_cmd, '-m', 'nuitka']
        # macos 和 非 macos icon 参数不同
        if platform.system() == 'Darwin':
            cmd_list += format_cmd('--macos-app-version=', self.product_version, self.product_version)
            cmd_list += format_cmd('--macos-app-icon=', self.icon_path.absolute(), self.icon_path)
        elif platform.system() == 'Windows':
            cmd_list += format_cmd('--windows-icon-from-ico=', self.icon_path.absolute(), self.icon_path)
        elif platform.system() == 'Linux':
            cmd_list += format_cmd('--linux-icon=', self.icon_path.absolute(), self.icon_path)

        cmd_list += format_cmd('lto=', 'yes' if self.use_lto else 'no')
        cmd_list += format_cmd('--clang' if self.use_clang else None)
        cmd_list += format_cmd('--msvc=latest' if self.use_msvc else None)
        cmd_list += format_cmd('--mingw64' if self.use_mingw else None)
        cmd_list += format_cmd('--standalone' if self.standalone else None)

        cmd_list += format_cmd('--disable-ccache' if not self.use_ccache else None)
        cmd_list += format_cmd('--show-progress' if self.show_progress else None)
        cmd_list += format_cmd('--show-memory' if self.show_memory else None)
        cmd_list += format_cmd('--remove-output' if self.remove_output else None)
        cmd_list += format_cmd('--assume-yes-for-download' if self.download_confirm else None)
        cmd_list += format_cmd('--run' if self.run_after_build else None)
        cmd_list += format_cmd('--enable-console' if self.enable_console else '--disable-console')

        cmd_list += format_cmd('--xml=', str(self.xml_path.absolute()), self.save_xml)
        cmd_list += format_cmd('--output_dir=', str(self.output_path.absolute()), self.output_path)
        cmd_list += format_cmd('--company-name=', self.company_name, self.company_name)
        cmd_list += format_cmd('--product-name=', self.product_name, self.product_name)
        cmd_list += format_cmd('--file-version=', str(self.file_version), self.file_version)
        cmd_list += format_cmd('--product-version=', str(self.product_version), self.product_version)
        cmd_list += format_cmd('--file-description=', self.file_description, self.file_description)
        cmd_list += format_cmd('--copy-right=', self.copy_right, self.copy_right)

        cmd_list += format_cmd('--follow-import-to=', self.follow_import, self.follow_import)
        cmd_list += format_cmd('--nofollow-import-to=', self.no_follow_import, self.no_follow_import)
        cmd_list += format_cmd('--enable-plugin=', self.enable_plugin, self.enable_plugin)
        cmd_list += format_cmd('--disable-plugin=', self.disable_plugin, self.disable_plugin)

        if self.include_data_dir:
            cmd_list += [f"--include-data-dir={src}={dst}" for src, dst in self.include_data_dir]
        if self.include_packages:
            cmd_list += [f"--include-package={package}" for package in self.include_packages]

        cmd_list.append(f"--main={self.src_file}")
        return cmd_list
