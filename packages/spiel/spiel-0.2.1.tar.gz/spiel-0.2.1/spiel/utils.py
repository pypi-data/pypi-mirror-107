from itertools import zip_longest
from typing import Any, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


def joinify(joiner: str, items: Iterable[Optional[Any]]) -> str:
    return joiner.join(map(str, filter(None, items)))


def drop_nones(*items: Optional[T]) -> Iterator[T]:
    yield from (item for item in items if item is not None)


def clamp(value: int, lower: int, upper: int) -> int:
    if lower > upper:
        raise ValueError(
            f"Upper bound ({upper}) for clamp must be greater than lower bound ({lower})."
        )
    return max(min(value, upper), lower)


def chunks(iterable: Iterable[T], n: int, fill_value: Optional[T] = None) -> Iterable[Iterable[T]]:
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fill_value)
