# pdm-packer

[![Tests](https://github.com/frostming/pdm-packer/workflows/Tests/badge.svg)](https://github.com/frostming/pdm-packer/actions?query=workflow%3Aci)
[![pypi version](https://img.shields.io/pypi/v/pdm-packer.svg)](https://pypi.org/project/pdm-packer/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/frostming/pdm-packer/main.svg)](https://results.pre-commit.ci/latest/github/frostming/pdm-packer/main)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

A PDM plugin that packs your packages into a zipapp

## Requirements

pdm-packer requires Python >=3.7

## Installation

If you have installed PDM with the recommended tool `pipx`, add this plugin by:

```bash
$ pipx inject pdm pdm-packer
```

Or if you have installed PDM with `pip install --user pdm`, install with `pip` to the user site:

```bash
$ python -m pip install --user pdm-packer
```

Otherwise, install `pdm-packer` to the same place where PDM is located.

## Usage

```
$ pdm pack [common-options] [pack-options]
```

**Common Options:**

`-h, --help`

> show this help message and exit

`-v, --verbose`

> -v for detailed output and -vv for more detailed

`-g, --global`

> Use the global project, supply the project
> root with `-p` option

`-p PROJECT_PATH, --project PROJECT_PATH`

> Specify another path as the project root,
> which changes the base of pyproject.toml and `__pypackages__`

**Pack Options:**

`-m MAIN, --main MAIN `

> Specify the console script entry point for
> the zipapp

`-o OUTPUT, --output OUTPUT`

> Specify the output filename. By default the file name
> will be inferred from the project name.

`-c, --compress`

> Compress files with the deflate method, no
> compress by default

`-i INTERPRETER, --interpreter INTERPRETER`

> The Python interpreter path, default: the
> project interpreter

`--exe`

> Create an executable file. If the output file
> isn't given, the file name will end with
> .exe(Windows) or no suffix(Posix)

See also: https://docs.python.org/3.9/library/zipapp.html

## Examples

```bash
# Create with default name(<project_name>.pyz) and console_script as the __main__.py
pdm pack
# Create an executable file
pdm pack --exe
# Create with custom __main__.py and filename
pdm pack -o app.pyz -m app:main
```

## About executable zipapp

By default, zipapp is created with `.pyz` suffix. On Windows, if you have associted `.pyz` files with Python program, you can run the app by double-clicking the file in the explorer. But if you create the app with `--exe` turn on, you can have a .exe file on Windows and an **executable** file
on Unix-like systems, so that the app can be executed without a `python` command prefixing it and
no matter you assoicated the file exensition properly or not.

## Changlog

See [CHANGELOG.md](https://github.com/frostming/pdm-packer/blob/main/CHANGELOG.md)
