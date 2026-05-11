# much simplified version of https://github.com/astral-sh/ruff-pre-commit/blob/main/mirror.py

from subprocess import run
import tomllib
from pathlib import Path
from urllib import request
from io import BytesIO
import json

def get_lib_version() -> str:
    with request.urlopen("https://crates.io/api/v1/crates/garbelour") as response:
        result = BytesIO(response.read())
    return json.loads(result.read())['crate']['max_stable_version']

def get_self_version() -> str:
    with open(Path(__file__).parent.parent.parent / "Cargo.toml", 'rb') as f:
        cargo = tomllib.load(f)
        for k, v in cargo["dependencies"].items():
            if k.startswith('garbelour'):
                return v

def update_cargo_toml(self_version: str, lib_version: str):
    with open('Cargo.toml') as f:
        content = f.read()
        content = content.replace(
            f'garbelour = "{self_version}"', f'garbelour = "{lib_version}"')
        content = content.replace(
            f'version = "{self_version}"', f'version = "{lib_version}"')

    with open('Cargo.toml', 'w') as f:
        f.write(content)

def copy_readme():
    src = 'garbelour-rs/README.md'
    dst = 'README.md'
    with open(src) as f:
        content = f.read()
    with open(dst, 'w') as f:
        f.write(content)

def main():
    lib_version = get_lib_version()
    self_version = get_self_version()
    print(f"garbelour-rs: {lib_version}, garbelour-py: {self_version}")

    if lib_version != self_version:
        update_cargo_toml(self_version, lib_version)
        copy_readme()



if __name__ == "__main__":
    main()
