# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinaturalist_convert']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict>=0.4.0,<0.5.0',
 'pyinaturalist==0.14.0.dev316',
 'tablib>=3.0.0,<4.0.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'all': ['gpxpy>=1.4.2,<2.0.0',
         'openpyxl>=2.6.0',
         'pandas>=1.2',
         'pyarrow>=4.0.0',
         'python-dwca-reader>=0.15.0,<0.16.0',
         'xmltodict>=0.12.0'],
 'df': ['pandas>=1.2'],
 'dwc': ['python-dwca-reader>=0.15.0,<0.16.0', 'xmltodict>=0.12.0'],
 'gpx': ['gpxpy>=1.4.2,<2.0.0'],
 'parquet': ['pandas>=1.2', 'pyarrow>=4.0.0'],
 'xlsx': ['openpyxl>=2.6.0']}

setup_kwargs = {
    'name': 'pyinaturalist-convert',
    'version': '0.0.1',
    'description': 'Pyinaturalist extensions to convert iNaturalist observation data to and from multiple formats ',
    'long_description': "# pyinaturalist-convert\n**This is an incomplete work in progress!**\n\n[Pyinaturalist](https://github.com/niconoe/pyinaturalist) extensions to convert iNaturalist observation data to and from multiple formats.\n\n# Formats\nImport formats currently supported:\n* CSV (Currently from API results only, but see planned features below)\n* JSON (either from a `requests.Response` or `pyinaturalist` results)\n* parquet\n\nExport formats currently supported:\n* CSV\n* Excel (xlsx)\n* GPX (experimental)\n* parquet\n* pandas DataFrame\n\n\n# Installation\n**Note:** PyPI release coming soon.\n```bash\npip install git+https://github.com/JWCook/pyinaturalist-convert.git\n```\n\nTo keep things modular, many format-specific dependencies are not installed by default, so you may need to install some\nmore packages depending on which formats you want. See [pyproject.toml](pyproject.toml) for the full list (TODO: docs on optional dependencies).\n\nTo install all of the things:\n```bash\npip install git+https://github.com/JWCook/pyinaturalist-convert.git#egg=pyinaturalist-convert[all]\n```\n\n# Usage\nBasic usage example:\n```python\nfrom pyinaturalist import get_observations\nfrom pyinaturalist_convert import to_csv\n\nobservations = get_observations(user_id='my_username')\nto_csv(observations, 'my_observations.csv')\n```\n\n# Planned/possible features\n* Convert to an HTML report\n* Convert to Simple Darwin Core format\n* Export to any [SQLAlchemy-compatible database engine](https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases)\n* Import and convert observation data from the [iNaturalist export tool](https://www.inaturalist.org/observations/export) and convert it to be compatible with observation data from the iNaturalist API\n* Import and convert metadata and images from [iNaturalist open data on Amazon]()\n    * See also [pyinaturalist-open-data](https://github.com/JWCook/pyinaturalist-open-data), which may eventually be merged with this package\n* Import and convert observation data from the [iNaturalist GBIF Archive](https://www.inaturalist.org/pages/developers)\n* Import and convert observation data from the[iNaturalist Taxonomy Archive](https://www.inaturalist.org/pages/developers)\n* Note: see [API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices)\n  for details on which data sources are best suited to different use cases\n\n",
    'author': 'Jordan Cook',
    'author_email': 'Jordan.Cook@pioneer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JWCook/pyinaturalist_convert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
