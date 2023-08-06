[![Tests](https://github.com/gmso/connect-4-cli/actions/workflows/python-package.yml/badge.svg)](https://github.com/gmso/connect-4-cli/actions/workflows/python-package.yml)
[![pypi package](https://github.com/gmso/connect-4-cli/actions/workflows/python-publish.yml/badge.svg)](https://github.com/gmso/connect-4-cli/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/connect-4-cli.svg)](https://badge.fury.io/py/connect-4-cli)
[![codecov](https://codecov.io/gh/gmso/connect-4-cli/branch/main/graph/badge.svg?token=9WO7IS1TN3)](https://codecov.io/gh/gmso/connect-4-cli)

# Connect 4 CLI
The classic 4-in-a-line game, also called connect 4, playable from the CLI or shell.

## Details
This is a simple implementation of the classic connect 4 game. It can be played directly from the CLI or shell.

## Installation
The game is available as a `pip` package. Download it with the following command:
```
pip install connect-4-cli
```

Preferably, install in [virtual environment](https://docs.python.org/3/library/venv.html).
In Windows, for example:
1. Run the following commands from the CLI:
```
py -m venv venv
```
2. Activate the virtual environment with the `activate` script inside the `./venv/Scripts/` folder:
   - Using command window: 
   ```
   call venv/Scripts/activate
   ```
   - Or using `powershell`:
   ```
   ./venv/Scripts/activate.ps1
   ```
3. `pip` install the package.

## How to play
Run the following command (with activated virtual environment if installed there) to start the game:
```
connect-4-cli
```
Play the game using keyboard keys, as prompted in the game.
