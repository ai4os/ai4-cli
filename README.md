# AI4 CLI tools and API library

[![GitHub license](https://img.shields.io/github/license/ai4os/ai4-cli.svg)](https://github.com/ai4os/ai4-cli/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/release/ai4os/ai4-cli.svg)](https://github.com/ai4os/ai4-cli/releases)
[![PyPI](https://img.shields.io/pypi/v/ai4-cli.svg)](https://pypi.python.org/pypi/ai4-cli)
[![Python versions](https://img.shields.io/pypi/pyversions/ai4-cli.svg)](https://pypi.python.org/pypi/ai4-cli)

Command line utilities for the AI4OS ([AI4EOSC](https://ai4eosc.eu/), [iMagine](https://imagine-ai.eu)) platforms.

## Installation

The reccomended way to install the AI4 CLI tools is using pip:

    $ pip install ai4-cli

## Configuration

The `ai4-cli` package will load the needed configuration from environment
variables whenever possible. In order to do so, it will read the `.env.ai4`
file in the current working directory, if it exists. If you want to use any
other file you can set the `AI4_DOTENV_FILE` environment variable to the path
of the file that you want to use.

The file can contain the following variables:

- `AI4_API_ENDPOINT`: The URL of the AI4OS compatible API.
- `AI4_API_VERSION`: The version of the API to use. Currently only `v1` is
  supported.
- `AI4_DEBUG`: If set to True, the CLI will output debug information.

## Usage

The `ai4-cli` package provides a set of subcommands that can be used to interact
with the AI4OS platform. The available subcommands can be listed using the
`ai4-cli --help` command.
