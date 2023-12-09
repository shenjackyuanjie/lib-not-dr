import sys
import subprocess

from typing import Union
from pathlib import Path


def clean(dir_path: Union[str, Path]):
    """
    clean everything in dir
    will not remove dir
    """
    print(f"Cleaning {dir_path}")
    path_dir = Path(dir_path) if isinstance(dir_path, str) else dir_path
    for path in path_dir.rglob("*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            clean(path)
            path.rmdir()


def clean_build():
    clean("./dist")
    clean("./build")


def upload_gitea():
    twine_cmd = [
        sys.executable,
        '-m', 'twine',
        'upload',
        '--repository',
        'gitea',
        './dist/*',
        '--verbose'
    ]
    subprocess.run(twine_cmd, shell=False, check=True)
