# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['load_testing_data_selectionsort']

package_data = \
{'': ['*'],
 'load_testing_data_selectionsort': ['load_testing_data/*',
                                     'load_testing_measurements/*',
                                     'load_testing_plots/*']}

install_requires = \
['click==7.1.2', 'matplotlib==3.4.2', 'numpy==1.20.3', 'pandas==1.2.4']

entry_points = \
{'console_scripts': ['create_chart = '
                     'load_testing_data_selectionsort.create_chart:main',
                     'generate_data = '
                     'load_testing_data_selectionsort.generate_data:main',
                     'measure_algo = '
                     'load_testing_data_selectionsort.measure_time:main',
                     'process_one = '
                     'load_testing_data_selectionsort.selection_sort:main']}

setup_kwargs = {
    'name': 'load-testing-data-selectionsort',
    'version': '0.1.0',
    'description': 'selection sort',
    'long_description': None,
    'author': 'AlexandrVolkov',
    'author_email': 'hramyh.w@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.9.5',
}


setup(**setup_kwargs)
