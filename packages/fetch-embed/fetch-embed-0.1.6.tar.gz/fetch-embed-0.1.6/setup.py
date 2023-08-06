# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetch_embed']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'httpx>=0.17.1,<0.18.0',
 'joblib>=1.0.1,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'logzero>=1.7.0,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'fetch-embed',
    'version': '0.1.6',
    'description': '',
    'long_description': '# fetch-embed\n<!--- fetch-embed  fetch_embed  fetch_embed fetch_embed --->\n[![tests](https://github.com/ffreemt/fetch-embed/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fetch_embed.svg)](https://badge.fury.io/py/fetch_embed)\n\nfetch multilingual embed from embed.ttw.workers.dev\n\n## Install it\n```bash\npip install -U fetch-embed\n```\n\n## Use it\n\n### Make use of the helper function `embed_text`\n\n#### `endpoints` for two models (dim-52 and dim-768)\n\nvia cloudflare: `https://embed.ttw.workers.dev/embed/` and `https://embed.ttw.workers.dev/embed_la/`\n\nIn case you cannot access `embed.ttw.workers.dev`, you may use `ttw.hopto.org` (hosted by noip.com) instead.\n\n##### Swagger UI: Self-docs for these endpoints\n[https://embed.ttw.workers.dev/docs](https://embed.ttw.workers.dev/docs)\n\n[https://ttw.hopto.org/docs](https://ttw.hopto.org/docs)\n\n#### Model 1: multilingual, dim-512\n\nThe default endpoint is `https://embed.ttw.workers.dev/embed/`\n```python\nfrom fetch_embed.embed_text import embed_text\n\nres = embed_text(["test a", "测试"])\nprint(res.shape)\n# (2, 512)\n```\n\n#### Model 2: language agnostic, dim-768\n\nendpoint: `https://embed.ttw.workers.dev/embed_la/`\n```python\nfrom fetch_embed.embed_text import embed_text\n\nendpoint = "https://embed.ttw.workers.dev/embed_la/"\n\nres = embed_text(["test a", "测试"], endpoint=endpoint)\nprint(res.shape)\n# (2, 768)\n```\n\nConsult the `embed_text.__doc__` (e.g. `print(embed_text.__doc__)`) or its source code for more details.\n\n### Access the API directly\n```python\nfrom fetch_embed import fetch_embed\n\nres = fetch_embed("test me")\nprint(res.shape)\n# (1, 512)\n\nprint(fetch_embed(["test me", "测试123"]).shape\n# (2, 512)\n\n# to turn off live progress bar\nres = fetch_embed("test me", livepbar=False)\n\n# brief docs\nhelp(fetch_embed)\n# fetch_embed(texts:Union[str, List[str]], endpoint:str=\'http://ttw.hopto.org/embed/\', livepbar:bool=True) -> numpy.ndarray\n    Fetch embed from endpoint.\n```\n\nPlug in `endpoint = "https://embed.ttw.workers.dev/embed_la/"` for Model 2, e.g.,\n```python\nimport numpy as np\nfrom fetch_embed import fetch_embed\n\nendpoint = "https://embed.ttw.workers.dev/embed_la/"\nres = fetch_embed("test me", endpoint=endpoint)\nprint(np.array(res).shape)\n# (1, 768)\n```',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/fetch-embed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
