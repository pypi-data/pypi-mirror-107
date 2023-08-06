# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alchemista']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'SQLAlchemy>=1.4.14,<2.0.0',
 'pydantic>=1.8.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.6.0,<4.0.0']}

setup_kwargs = {
    'name': 'alchemista',
    'version': '0.2.1',
    'description': 'Tools to convert SQLAlchemy models to Pydantic models',
    'long_description': '# Alchemista\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/ggabriel96/alchemista/branch/main/graph/badge.svg?token=MYXKIH09FJ)](https://codecov.io/gh/ggabriel96/alchemista)\n\nTools to generate Pydantic models from SQLAlchemy models.\n\nStill experimental.\n\n## Installation\n\nAlchemista is [available in PyPI](https://pypi.org/project/alchemista/).\nTo install it with `pip`, run:\n\n\n```shell\npip install alchemista\n```\n\n## Usage\n\nSimply call the `model_from` function with a SQLAlchemy model.\nEach `Column` in its definition will result in an attribute of the generated model via the Pydantic `Field` function.\n\nFor example, a SQLAlchemy model like the following\n\n```python\nfrom sqlalchemy import Column, Integer, String\nfrom sqlalchemy.orm import declarative_base\n\n\nBase = declarative_base()\n\nclass PersonDB(Base):\n    __tablename__ = "people"\n\n    id = Column(Integer, primary_key=True)\n    age = Column(Integer, default=0, nullable=False, doc="Age in years")\n    name = Column(String(128), nullable=False, doc="Full name")\n```\n\ncould have a generated Pydantic model via\n\n```python\nfrom alchemista import model_from\n\nPerson = model_from(PersonDB)\n```\n\nand would result in a Pydantic model equivalent to\n\n```python\nfrom pydantic import BaseModel, Field\n\n\nclass Person(BaseModel):\n    id: int\n    age: int = Field(0, description="Age in years")\n    name: str = Field(..., max_length=128, description="Full name")\n\n    class Config:\n        orm_mode = True\n```\n\nNote that the string length from the column definition was sufficient to add a `max_length` constraint.\nAdditionally, by default, the generated model will have `orm_mode=True`.\nThat can be customized via the `__config__` keyword argument.\n\nThere is also an `exclude` keyword argument that accepts a set of field names to _not_ include in the generated model,\nand an `include` keyword argument accepts a set of field names to _do_ include in the generated model.\nHowever, they are mutually exclusive and cannot be used together.\n\nThis example is available in a short executable form in the [`examples/`](examples/) directory.\n\n## `Field` arguments and `info`\n\nCurrently, the type, default value (either scalar or callable), and the description (from the `doc` attribute) are\nextracted directly from the `Column` definition.\nHowever, except for the type, all of them can be overridden via the `info` dictionary attribute.\nAll other custom arguments to the `Field` function are specified there too.\nThe supported keys are listed in `alchemista.field.Info`.\n\n**Everything specified in `info` is preferred from what has been extracted from `Column`**.\nThis means that the default value and the description can be **overridden** if so desired.\nAlso, similarly to using Pydantic directly, `default` and `default_factory` are mutually-exclusive,\nso they cannot be used together.\nUse `default_factory` if the default value comes from calling a function (without any arguments).\n\nFor example, in the case above,\n\n```python\nname = Column(String(128), nullable=False, doc="Full name", info=dict(description=None, max_length=64))\n```\n\nwould instead result in\n\n```python\nname: str = Field(..., max_length=64)\n```\n\n## `fields_from` and `model_from`\n\nThe `fields_from` function is the function that actually inspects the SQLAlchemy model and builds a dictionary\n    in a format that can be used to generate a Pydantic model.\nSo `model_from` is just a shortcut for calling `fields_from` and then `pydantic.create_model`.\nThe model name that `model_from` sets is `db_model.__name__`.\n\nIf desired, or extra control is needed, `pydantic.create_model` can be used directly, in conjunction with `fields_from`.\nThis allows the customization of the name of the model that will be created and the specification of other\n    `create_model` arguments, like `__base__` and `__validators__` (`model_from` currently only accepts `__config__`).\n\nFor example:\n\n```python\nfrom alchemista import fields_from\nfrom pydantic import create_model\n\n\nMyModel = create_model("MyModel", **fields_from(DBModel))\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Gabriel Galli',
    'author_email': 'ggabriel96@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggabriel96/alchemista',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
