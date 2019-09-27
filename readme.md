# Python CLI examples
This repository contains examples of usage of most popular Python CLI frameworks,
such as:

* [argparse](https://docs.python.org/3/library/argparse.html)
* [cliff](https://github.com/openstack/cliff)
* [plac](https://github.com/micheles/plac)
* [plumbum](https://github.com/tomerfiliba/plumbum)
* [cmd2](https://github.com/python-cmd2/cmd2/)
* [urwid](https://github.com/urwid/urwid)


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
python todo_plac.py show
# etc
```