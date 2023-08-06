# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frozen_data']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0']

setup_kwargs = {
    'name': 'djang-frozen-data',
    'version': '0.1a1',
    'description': 'Django model field used to store snapshot of data.',
    'long_description': '# Django Frozen Data\n\nDjango model custom field for storing a frozen snapshot of an object.\n\n## Principles\n\n* Behaves _like_ a `ForeignKey` but the data is detached from the related object\n* Transparent to the client - it looks and behaves like the original object\n* The frozen object cannot be resaved\n* Supports nesting of objects\n\n## Usage\n\nA frozen field can be declared like a `ForeignKey`:\n\n```python\nclass Foo:\n    frozen_bar = FrozenObjectField(Bar, help_text="This is a frozen snapshot of the object.")\n    fresh_bar = ForeignKey(Bar, help_text="This is a live FK relationship.")\n```\n\nThe field behaves exactly like a FK, with the exception that the object cannot be saved:\n\n```python\n>>> bar = Bar()\n>>> foo = Foo.objects.create(frozen_bar=bar, fresh_bar=bar)\n>>> # the fresh field can be updated as you would expect\n>>> foo.fresh_bar.save()\n>>> # the frozen field cannot - to prevent overwriting new data.\n>>> foo.frozen_bar.save()\n>>> StaleObjectError: \'Object was frozen; defrosted objects cannot be saved.\'\n```\n\n### Issues - TODO\n\n- [x] Deserialization of DateField/DateTimeField values\n- [x] Deserialization of DecimalField values\n- [x] Deserialization of UUIDField values\n- [ ] Deep object freezing\n\n#### Running tests\n\nThe tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment, you can run them thus:\n\n```\n$ poetry run pytest\n```\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-frozen-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
