# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'random-tools',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Random Tools\n\n[![Build Status](https://api.travis-ci.org/rallesiardo/random_tools.svg?branch=master)](https://travis-ci.org/rallesiardo/random_tools)\n[![PyPI version](https://badge.fury.io/py/random-tools.svg)](https://badge.fury.io/py/random-tools)\n\n\n## random_tools.Signal\n\n```python\nfrom random_tools import Signal\n\non_event = Signal()\non_event.connect(print)\non_event.emit("this will be printed")\n\n```\n\n## random_tools.true_every\n\n```python\nfrom random_tools import true_every\n\nthis_true_every_3_calls = true_every(3) # will return True every 3 calls\n\nfalse_1 = next(this_true_every_3_calls) # False\nfalse_2 = next(this_true_every_3_calls) # False\n\ntrue_1 = next(this_true_every_3_calls) # True\n\nfalse_3 = next(this_true_every_3_calls) # False\nfalse_4 = next(this_true_every_3_calls) # False\n\ntrue_2 = next(this_true_every_3_calls) # True\n\n```\n\n## random_tools.CSS4_ColorPicker\nA tool for sampling CSS4 compatible color names\n\n```python\nfrom random_tools import CSS4_ColorPicker\n\n    color_picker = CSS4_ColorPicker()\n\n    colors = set()\n    for i in range(nb_color):\n        color = color_picker.sample_color()\n        assert color not in colors\n        colors.add(color)\n        \n    # The picker reset automatiquely when all color have been sampled\n    #  but you can reset it manually too\n    color_picker.reset()\n\n```',
    'author': 'Robin Allesiardo',
    'author_email': 'robin.allesiardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rallesiardo/random_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
