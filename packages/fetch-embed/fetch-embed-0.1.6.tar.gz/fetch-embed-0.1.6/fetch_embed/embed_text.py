"""Embed Embed batch of text (bsize=32) to np.ndarray."""
from typing import List, Union
import numpy as np
import more_itertools as mit
from tqdm import tqdm
from joblib import Memory
import httpx

from loguru import logger

from fetch_embed import fetch_embed

location = "./joblibcache"
memory = Memory(location, verbose=0)


# fmt: off
@memory.cache
def embed_text(
        src_blocks: Union[str, List[str]],
        bsize:int = 32,
        endpoint: str = None,
        timeout = httpx.Timeout(15, read=300),
) -> np.ndarray:
    # fmt on
    """Embed batch of text (bsize=32)."""
    if isinstance(src_blocks, str):
        src_blocks = [src_blocks]

    src_embed = []
    len_ = len(src_blocks)
    tot = len_ // bsize + bool(len_ % bsize)
    idx = 0
    pbar = tqdm(total=tot)
    for elm in mit.chunked(src_blocks, bsize):
        idx += 1
        logger.debug(" {}, {}".format(idx, idx / tot))
        try:
            if endpoint is None:
                _ = fetch_embed(elm, livepbar=False, timeout=timeout)
            else:
                _ = fetch_embed(elm, livepbar=False, endpoint=endpoint, timeout=timeout)
        except Exception as e:
            logger.error(e)
            # _ = [[str(e)] + [""] * 31]
            raise
        src_embed.extend(_)
        pbar.update()
    return np.array(src_embed)
