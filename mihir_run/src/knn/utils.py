import asyncio
import base64
import functools
import io
import itertools
import textwrap
import traceback

import numpy as np

from typing import Any, Awaitable, AsyncIterable, List, Union, Dict, Iterator

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


class FileListIterator:
    def __init__(self, list_path: str, map_fn=lambda line: line) -> None:
        self.map_fn = map_fn

        self._list = open(list_path, "r")
        self._total = 0
        for line in self._list:
            if not line.strip():
                break
            self._total += 1
        self._list.seek(0)

    def close(self, *args, **kwargs):
        self._list.close()

    def __len__(self):
        return self._total

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        elem = self._list.readline().strip()
        if not elem:
            raise StopIteration
        return self.map_fn(elem)


# TODO(mihirg): Fix this!
class LimitedAsCompletedIterator:
    def __init__(self, coros: AsyncIterable[Awaitable[Any]], limit: int):
        self.coros = coros
        self.limit = limit

        self.pending: List[asyncio.Task] = []
        self.hit_stop_iteration = False
        self.next_coro_is_pending = False

    async def _get_next_coro(self):
        try:
            return await self.coros.__anext__()
        except StopAsyncIteration:
            self.hit_stop_iteration = True

    def _schedule_getting_next_coro(self):
        task = asyncio.create_task(self._get_next_coro())
        task.is_to_get_next_coro = True
        self.pending.append(task)
        self.next_coro_is_pending = True

    def __aiter__(self):
        self.coros = self.coros.__aiter__()
        self._schedule_getting_next_coro()
        return self

    async def __anext__(self):
        while self.pending:
            print(len(self.pending))

            done, self.pending = await asyncio.wait(
                self.pending, return_when=asyncio.FIRST_COMPLETED
            )
            assert len(done) == 1
            done = next(iter(done))
            self.pending = list(self.pending)

            if getattr(done, "is_to_get_next_coro", False):
                self.next_coro_is_pending = False
                if self.hit_stop_iteration:
                    continue

                # Schedule the new coroutine
                self.pending.append(asyncio.create_task(done.result()))

                # If we have capacity, also ask for the next coroutine
                if len(self.pending) < self.limit:
                    self._schedule_getting_next_coro()
            else:
                # We definitely have capacity now, so ask for the next coroutine if we
                # haven't already
                if not self.next_coro_is_pending and not self.hit_stop_iteration:
                    self._schedule_getting_next_coro()

                return done.result()

        raise StopAsyncIteration


async def limited_as_completed(coros, limit):
    # Based on https://github.com/andybalaam/asyncioplus/blob/master/asyncioplus/limited_as_completed.py  # noqa
    futures = [asyncio.create_task(c) for c in itertools.islice(coros, 0, limit)]
    pending = [len(futures)]  # list so that we can modify from first_to_finish

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for i, f in enumerate(futures):
                if f is not None and f.done():
                    try:
                        newf = next(coros)
                        futures[i] = asyncio.create_task(newf)
                    except StopIteration:
                        futures[i] = None
                        pending[0] -= 1
                    return f.result()

    while pending[0] > 0:
        yield (await first_to_finish())


def chunk(it, chunk_size, until=None):
    n = 0
    while True:
        this_chunk_size = chunk_size
        if until:
            if n >= until:
                break
            this_chunk_size = min(this_chunk_size, until - n)

        chunk = list(itertools.islice(it, this_chunk_size))
        if not chunk:
            break
        n += len(chunk)
        yield chunk


def unasync(coro):
    @functools.wraps(coro)
    def wrapper(*args, **kwargs):
        return asyncio.run(coro(*args, **kwargs))

    return wrapper


def unasync_as_task(coro):
    @functools.wraps(coro)
    def wrapper(*args, **kwargs):
        return asyncio.create_task(coro(*args, **kwargs))

    return wrapper


def log_exception_from_coro_but_return_none(coro):
    @functools.wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            return await coro(*args, **kwargs)
        except Exception:
            print(f"Error from {coro.__name__}")
            print(textwrap.indent(traceback.format_exc(), "  "))
        return None

    return wrapper


def numpy_to_base64(nda):
    with io.BytesIO() as nda_buffer:
        np.save(nda_buffer, nda, allow_pickle=False)
        nda_bytes = nda_buffer.getvalue()
        nda_base64 = base64.b64encode(nda_bytes).decode("ascii")
    return nda_base64


def base64_to_numpy(nda_base64):
    nda_bytes = base64.b64decode(nda_base64)
    with io.BytesIO(nda_bytes) as nda_buffer:
        nda = np.load(nda_buffer, allow_pickle=False)
    return nda
