# fetch-embed
<!--- fetch-embed  fetch_embed  fetch_embed fetch_embed --->
[![tests](https://github.com/ffreemt/fetch-embed/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fetch_embed.svg)](https://badge.fury.io/py/fetch_embed)

fetch multilingual embed from embed.ttw.workers.dev

## Install it
```bash
pip install -U fetch-embed
```

## Use it

### Make use of the helper function `embed_text`

#### `endpoints` for two models (dim-52 and dim-768)

via cloudflare: `https://embed.ttw.workers.dev/embed/` and `https://embed.ttw.workers.dev/embed_la/`

In case you cannot access `embed.ttw.workers.dev`, you may use `ttw.hopto.org` (hosted by noip.com) instead.

##### Swagger UI: Self-docs for these endpoints
[https://embed.ttw.workers.dev/docs](https://embed.ttw.workers.dev/docs)

[https://ttw.hopto.org/docs](https://ttw.hopto.org/docs)

#### Model 1: multilingual, dim-512

The default endpoint is `https://embed.ttw.workers.dev/embed/`
```python
from fetch_embed.embed_text import embed_text

res = embed_text(["test a", "测试"])
print(res.shape)
# (2, 512)
```

#### Model 2: language agnostic, dim-768

endpoint: `https://embed.ttw.workers.dev/embed_la/`
```python
from fetch_embed.embed_text import embed_text

endpoint = "https://embed.ttw.workers.dev/embed_la/"

res = embed_text(["test a", "测试"], endpoint=endpoint)
print(res.shape)
# (2, 768)
```

Consult the `embed_text.__doc__` (e.g. `print(embed_text.__doc__)`) or its source code for more details.

### Access the API directly
```python
from fetch_embed import fetch_embed

res = fetch_embed("test me")
print(res.shape)
# (1, 512)

print(fetch_embed(["test me", "测试123"]).shape
# (2, 512)

# to turn off live progress bar
res = fetch_embed("test me", livepbar=False)

# brief docs
help(fetch_embed)
# fetch_embed(texts:Union[str, List[str]], endpoint:str='http://ttw.hopto.org/embed/', livepbar:bool=True) -> numpy.ndarray
    Fetch embed from endpoint.
```

Plug in `endpoint = "https://embed.ttw.workers.dev/embed_la/"` for Model 2, e.g.,
```python
import numpy as np
from fetch_embed import fetch_embed

endpoint = "https://embed.ttw.workers.dev/embed_la/"
res = fetch_embed("test me", endpoint=endpoint)
print(np.array(res).shape)
# (1, 768)
```