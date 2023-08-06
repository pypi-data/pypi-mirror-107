# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightshield', 'lightshield.proxy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'aioredis>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'lightshield',
    'version': '0.1.6b0',
    'description': 'Library part of the Lightshield tool.',
    'long_description': "## Lightshield Tools\n\nTools and Code-Sections of the Lightshield Framework that were better fit to be provided through dependency\nrather then included in the main project.\n\n#### What currently doesn't work:\n- The keys used to save data in Redis are not linked to the API key, as such multiple keys have to use\nmultiple Redis servers.\n\n### Ratelimiter (WIP)\n\nMulti-Host async ratelimiting service. The clients each sync via a central redis server. \n\nSet up the proxy in an async context with redis connection details.\n```python\nfrom lightshield.proxy import Proxy\nimport aiohttp\n\nasync def run():\n    p = Proxy()\n    # Initiate the redis connector in async context\n    await p.init(host='localhost', port=5432)\n```\n\nMake singular calls directly through the Proxy.\n```python\nasync with aiohttp.ClientSession(headers={'X-Riot-Token': ''}) as session:\n    await p.request('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/SILVER/I', session=session)\n```\n\nMake calls directly to one endpoint without having the proxy select the proper limits \nthrough a regex comparison to increase processing speed.\n```python\nasync with aiohttp.ClientSession(headers={'X-Riot-Token': ''}) as session:\n    zone = await p.get_endpoint('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/')\n    for page in range(1, 10):\n        zone.request('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/SILVER/I?page=%s' % page, session)\n```\n\n### Settings (WIP)\nThe settings file contains a number of variables that are used across the project.\nVariables can be set through:  \n`ENV > config.json > default`\n```python\nfrom lightshield import settings\n\nheaders = {'X-Riot-Token': settings.API_KEY}\n```\n",
    'author': 'Doctress',
    'author_email': 'lightshielddev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LightshieldDotDev/Lightshield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
