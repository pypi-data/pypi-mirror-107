"""Fetch embed from endpoint."""
from typing import List, Union

# from math import ceil
import platform
import httpx

from logzero import logger
from alive_progress import alive_bar

HOST1 = "ttw.hopto.org"
HOST2 = "embed.ttw.workers.dev"
EP1 = f"http://{HOST1}/embed/"
EP2 = f"http://{HOST2}/embed/"
TIMEOUT = httpx.Timeout(15, read=300)  # 5min read timeout, 15s
CLIENT = httpx.Client(verify=False, timeout=TIMEOUT)

EP_ = ""
# if in oracle2, use 127.0.0.1:8000
if platform.node() == "oracle2":
    EP_ = f"http://127.0.0.1:8000/embed/"

if not EP_:
    try:
        httpx.get(EP1)
        EP_ = EP1
    except Exception:
        EP_ = EP2


# fmt: off
def fetch_embed(
        texts: Union[str, List[str]],
        endpoint: str = EP_,
        livepbar: bool = True,  # need to turned off for pytest
        timeout=TIMEOUT,
        client=CLIENT,
) -> List[float]:
    """Fetch embed from endpoint."""
    if isinstance(texts, str):
        texts = [texts]
    data = {"text1": texts}

    if len(data) > 32:
        logger.warning("This will likely result in timeout errors")
        logger.warning("You may wish to break down to smaller pieces.")
        raise Exception("List too long")

    resp = httpx.Response(200)


    def func_():
        nonlocal resp
        try:
            # resp = httpx.post(
            resp = client.post(
                endpoint,
                json=data,
                timeout=timeout)
            resp.raise_for_status()
        except Exception as exc:
            logger.error(exc)
            # msg = str(exc)
            raise

    if livepbar:
        with alive_bar(1, length=3) as pbar:
            func_()
            pbar()
    else:
        func_()

    try:
        jdata = resp.json()
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        res = jdata.get("embed")
    except Exception as e:
        logger.error(e)
        raise

    if res is None:
        raise Exception("Cant get anything from jdata.get('embed'), probably wrong API...")

    # return np.array(res)
    return res

    # feed back error messages
    # return np.array([jdata.get("error")])
