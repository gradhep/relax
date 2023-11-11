from __future__ import annotations

__all__ = ("relaxed_of", "unrelaxed")

from contextlib import contextmanager
from functools import wraps
from typing import Callable, Generator, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


_is_relaxed: bool = True


# Invoked with relaxed_of(unrelaxed_func)
def relaxed_of(unrelaxed: Callable[P, R]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    # Returns wrapper that accepts relaxed implementation
    def wrapper(impl: Callable[P, R]) -> Callable[P, R]:
        # This wrapper returns the context-aware fn that delegates between impl and unrelaxed
        @wraps(impl)
        def delegate(*args: P.args, **kwargs: P.kwargs) -> R:
            if _is_relaxed:
                return impl(*args, **kwargs)
            return unrelaxed(*args, **kwargs)

        return delegate

    return wrapper


@contextmanager
def unrelaxed(unrelaxed: bool = True) -> Generator[None, None, None]:
    """Temporarily set the unrelaxed context"""
    global _is_relaxed
    old_state: bool = _is_relaxed
    _is_relaxed = not unrelaxed
    yield
    _is_relaxed = old_state
