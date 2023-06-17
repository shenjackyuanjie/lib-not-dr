#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# 用于使用 nuitka 构建 DR
import platform
import traceback
from pathlib import Path
from typing import List, Tuple, Optional

from lib_not_dr.types import Options, Version


def _add_cmd(cmd: List[str], string: Optional[str]) -> List[str]:
    if string is not None and string:
        cmd.append(string)
    return cmd


class CompilerHelper(Options):
    name = 'Nuitka Compiler Helper'

    output_path: Path = Path('./build')
    src_file: Path

    python_cmd: str = 'python'

    # 以下为 nuitka 的参数
    use_lto: bool = False  # --lto=yes (no is faster)
    use_clang: bool = True  # --clang
    use_msvc: bool = True  # --msvc=latest
    use_mingw: bool = False  # --mingw64
    standalone: bool = True  # --standalone
    use_ccache: bool = True  # not --disable-ccache
    enable_console: bool = True  # --enable-console / --disable-console

    show_progress: bool = True  # --show-progress
    show_memory: bool = False  # --show-memory
    save_xml: bool = False  # --xml
    xml_path: Path = Path('build/compile_data.xml')

    download_confirm: bool = True  # --assume-yes-for-download

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
        front = super().as_markdown(longest)
        gen_cmd = self.gen_subprocess_cmd()
        return f"{front}\n\n```bash\n{' '.join(gen_cmd)}\n```"

    def gen_subprocess_cmd(self) -> List[str]:
        cmd_list = [self.python_cmd, '-m', 'nuitka']
        # macos 和 非 macos icon 参数不同
        if platform.system() == 'Darwin':
            cmd_list.append(f"--macos-app-version={self.product_version}")
            _add_cmd(cmd_list, f'--macos-app-icon={self.icon_path.absolute()}' if self.icon_path else None)
        elif platform.system() == 'Windows':
            _add_cmd(cmd_list, f'--windows-icon-from-ico={self.icon_path.absolute()}' if self.icon_path else None)
        elif platform.system() == 'Linux':
            _add_cmd(cmd_list, f'--linux-icon={self.icon_path.absolute()}' if self.icon_path else None)

        _add_cmd(cmd_list, '--lto=yes' if self.use_lto else '--lto=no')
        _add_cmd(cmd_list, '--clang' if self.use_clang else None)
        _add_cmd(cmd_list, '--msvc=latest' if self.use_msvc else None)
        _add_cmd(cmd_list, '--mingw64' if self.use_mingw else None)
        _add_cmd(cmd_list, '--standalone' if self.standalone else None)

        _add_cmd(cmd_list, '--disable-ccache' if not self.use_ccache else None)
        _add_cmd(cmd_list, '--show-progress' if self.show_progress else None)
        _add_cmd(cmd_list, '--show-memory' if self.show_memory else None)
        _add_cmd(cmd_list, '--assume-yes-for-download' if self.download_confirm else None)
        _add_cmd(cmd_list, '--enable-console' if self.enable_console else '--disable-console')

        _add_cmd(cmd_list, f'--xml={self.xml_path.absolute()}' if self.save_xml else None)
        _add_cmd(cmd_list, f'--output-dir={self.output_path.absolute()}' if self.output_path else None)
        _add_cmd(cmd_list, f'--company-name={self.company_name}' if self.company_name else None)
        _add_cmd(cmd_list, f'--product-name={self.product_name}' if self.product_name else None)
        _add_cmd(cmd_list, f'--file-version={self.file_version}' if self.file_version else None)
        _add_cmd(cmd_list, f'--product-version={self.product_version}' if self.product_version else None)
        _add_cmd(cmd_list, f'--file-description={self.file_description}' if self.file_description else None)
        _add_cmd(cmd_list, f'--copyright={self.copy_right}' if self.copy_right else None)

        _add_cmd(cmd_list, f'--follow-import-to={",".join(self.follow_import)}' if self.follow_import else None)
        _add_cmd(cmd_list, f'--nofollow-import-to={",".join(self.no_follow_import)}' if self.no_follow_import else None)
        _add_cmd(cmd_list, f'--enable-plugin={",".join(self.enable_plugin)}' if self.enable_plugin else None)
        _add_cmd(cmd_list, f'--disable-plugin={",".join(self.disable_plugin)}' if self.disable_plugin else None)

        if self.include_data_dir:
            cmd_list += [f"--include-data-dir={src}={dst}" for src, dst in self.include_data_dir]
        if self.include_packages:
            cmd_list += [f"--include-package={package}" for package in self.include_packages]

        cmd_list.append(f"{self.src_file}")
        return cmd_list


if __name__ == '__main__':
    cp = CompilerHelper(src_file = Path('test.py'))
    print(cp)

