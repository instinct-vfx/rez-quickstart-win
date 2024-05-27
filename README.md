# rez-quickstart-win 
rez-quickstart-win is a simple and easy replacement for `rez-bind --quickstart`.
The latter is both broken (especially on windows) and to be deprecated.

rez-quickstart-win will create packages for `platform`, `arch`, `os` and `python`.

Note: `python2`is currently not supported, neither for running rez-quickstart-win
nor as a python package version.

# Installation

```
pip install rez-quickstart-win
```

# Usage

Running rez-quickstart-win without any parameters (`rez-quickstart`) will create
rez packages and a python package for the latest (non-pre-release) python version
available on nuget.

By default packages are created in your local package folder, if you add `-r`
packages will be released to the configured release packages path. In addition
you can also provide a target path manually using `-p`.

```
Usage: rez-quickstart [OPTIONS]

Options:
  -r, --release             Release to release path instead of local path
  -p, --packages_path TEXT  Release to custom path, overrides --release
  --python_version TEXT     Release specific version (latest if not set)
  --help                    Show this message and exit.
```