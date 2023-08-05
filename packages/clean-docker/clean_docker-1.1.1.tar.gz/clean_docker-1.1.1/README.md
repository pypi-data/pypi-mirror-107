# clean-docker

Basic script to get rid of Docker images, containers, volumes, and networks

## Installation

`pip install -U --user clean-docker`

> The package will be installed in your user home directory. See `pip`
> documentation about [user installs][1]. You need the installation directory
> to be present in `PATH` to run `clean-docker` from the terminal.

## Usage

```console
$ clean-docker --help
Usage: clean-docker [OPTIONS]

  Remove Docker images, containers, volumes, and networks

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

## Requirements

- Tested with Python 3.9+
- You need a Docker daemon running on your machine

[1]: https://pip.pypa.io/en/latest/user_guide/#user-installs
