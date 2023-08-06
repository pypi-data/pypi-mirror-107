# mmhelloworld
Trying uploading to pypi a hello world package.

## Installation
Run the following to install:

```python
pip install mmhelloworld
```

## Usage
```python
from mmhelloworld import say_hello

# Prefer to paste logs from ipython.

# Prints "Hello! World"
say_hello()

# Prints "Hello! Everybody"
say_hello('Everybody')
```

# Developing Hello World
To install hello world along with tools you need to develop and run tests, run the following in your virtualenv.
```bash
$ pip install -e .[dev]
```

