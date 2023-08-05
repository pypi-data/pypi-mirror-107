[![](https://img.shields.io/pypi/v/import-submodules.svg?maxAge=3600)](https://pypi.org/project/import-submodules/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)

### Installation
```bash
$ pip install import-submodules
```

### Pros
replaces multiple imports with one line

### Examples
```
folder
├── __init__.py
├── module1.py
├── module2.py
└── module3.py
```

`__init__.py`
```python
import import_submodules

import_submodules.import_submodules()           # import moduleX
```
```python
import import_submodules

import_submodules.import_all_from_submodules()  # from moduleX import *
```

