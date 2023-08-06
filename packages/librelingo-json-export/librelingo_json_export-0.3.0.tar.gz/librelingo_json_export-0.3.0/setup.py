# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_json_export']

package_data = \
{'': ['*']}

install_requires = \
['librelingo-types>=1.0.0,<2.0.0',
 'librelingo-utils>=2.0.0,<3.0.0',
 'librelingo-yaml-loader>=1.0.0,<2.0.0',
 'python-slugify>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'librelingo-json-export',
    'version': '0.3.0',
    'description': 'Export LibreLingo courses in the JSON format used by the web app',
    'long_description': '<a name="librelingo_json_export.challenges"></a>\n# librelingo\\_json\\_export.challenges\n\n<a name="librelingo_json_export.challenges.make_challenges_using"></a>\n#### make\\_challenges\\_using\n\n```python\nmake_challenges_using(callback, data_source, course)\n```\n\nCalls a callback function with an item (Word or Phrase)\nto create challenges. Each item in the data source will\nbe used.\n\n<a name="librelingo_json_export.challenges.challenge_mapper"></a>\n#### challenge\\_mapper\n\n```python\nchallenge_mapper(challenge_types)\n```\n\nReturns a function that applies challenge types\nto a certain item (Word or Phrase), using the settings\nof the given course.\n\n<a name="librelingo_json_export.challenges.get_challenges_data"></a>\n#### get\\_challenges\\_data\n\n```python\nget_challenges_data(skill, course)\n```\n\nGenerates challenges for a certain Skill\n\n<a name="librelingo_json_export.export"></a>\n# librelingo\\_json\\_export.export\n\n<a name="librelingo_json_export.export.export_course"></a>\n#### export\\_course\n\n```python\nexport_course(export_path, course, settings=None)\n```\n\nWrites the course to JSON files in the specified path.\n\n### Usage example:\n\n```python\nfrom librelingo_yaml_loader import load_course\nfrom librelingo_json_export.export import export_course\n\ncourse = load_course("./courses/french-from-english")\nexport_course("./apps/web/src/courses/french-from-english", course)\n```\n\n',
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
