# Python CLI examples
This repository contains examples of usage of most popular Python CLI frameworks,
such as:

* [argparse](https://docs.python.org/3/library/argparse.html)
* [docopt](https://github.com/docopt/docopt)
* [click](https://github.com/pallets/click)
* [fire](https://github.com/google/python-fire)
* [cement](https://github.com/datafolklabs/cement)
* [cleo](https://github.com/sdispater/cleo)
* And more (later)!

## Installation
Python 3.7 required.
```bash
python3.7 -m venv .venv
.venv/bin/pip install .
```

## Usage
```bash
source .venv/bin/activate
python todo_argparse.py add test
python todo_click.py show
# etc
```