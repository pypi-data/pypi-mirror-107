# secondstate

[![GitHub release](https://img.shields.io/github/release/fruiti-ltd/secondstate.svg)](https://gitHub.com/fruiti-ltd/secondstate/releases/)
[![PyPI version](https://badge.fury.io/py/secondstate.svg)](https://badge.fury.io/py/secondstate)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/fruiti-ltd/secondstate.svg)](https://gitHub.com/fruiti-ltd/secondstate/pull/)
![Build](https://github.com/fruiti-ltd/secondstate/actions/workflows/build.yml/badge.svg)
![Release](https://github.com/fruiti-ltd/secondstate/actions/workflows/release.yml/badge.svg)
[![GitHub license](https://img.shields.io/github/license/fruiti-ltd/secondstate.svg)](https://github.com/fruiti-ltd/blob/main/LICENSE)

## Requirements

- Python >= 3.8
- [Docker](https://docker.com) (for development only)

## Installation

    pip install secondstate

## Usage

Lets say you want to figure out the availability of a haircut with a particular barber:

```python
from secondstate import SecondState

# We want all available appointments from now until the next 7 days
barber = SecondState(start="2021-05-23T11:17:49", finish="2021-05-30T11:17:49")

# The barber works Monday 10:00-16:00
barber.set(start="2021-05-24T10:00:00", finish="2021-05-24T16:00:00")

# Looks like the barber already has appointments on Monday at 10:30 and 15:00
barber.unset(start="2021-05-24T10:30:00", finish="2021-05-24T11:00:00")
barber.unset(start="2021-05-24T15:00:00", finish="2021-05-24T15:30:00")

# Haircut takes 30 minutes
print(barber.get(minutes=30))

```

Result:

```bash
[
    ["2021-05-24T10:00:00", "2021-05-24T10:30:00"],
    ["2021-05-24T11:00:00", "2021-05-24T11:30:00"],
    ["2021-05-24T11:30:00", "2021-05-24T12:00:00"],
    ["2021-05-24T12:00:00", "2021-05-24T12:30:00"],
    ["2021-05-24T12:30:00", "2021-05-24T13:00:00"],
    ["2021-05-24T13:00:00", "2021-05-24T13:30:00"],
    ["2021-05-24T13:30:00", "2021-05-24T14:00:00"],
    ["2021-05-24T14:00:00", "2021-05-24T14:30:00"],
    ["2021-05-24T14:30:00", "2021-05-24T15:00:00"],
    ["2021-05-24T15:30:00", "2021-05-24T16:00:00"],
]
```

To use the development environment:

    make dev

## Releasing

    poetry version major | minor | patch
    make release
