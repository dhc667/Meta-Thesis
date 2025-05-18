from typing import Generic, TypeVar, Optional, Callable

T = TypeVar("T")  # Original value type
U = TypeVar("U")  # Mapped value type
E = TypeVar("E")  # Error type

class Result(Generic[T, E]):
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Use Result.new_ok() or Result.new_err()")

    def _init(self, ok: Optional[T] = None, err: Optional[E] = None):
        self._ok = ok
        self._err = err

    @staticmethod
    def new_ok(value: T) -> "Result[T, E]":
        r = object.__new__(Result)
        r._init(ok=value)
        return r

    @staticmethod
    def new_err(error: E) -> "Result[T, E]":
        r = object.__new__(Result)
        r._init(err=error)
        return r

    def is_ok(self) -> bool:
        return self._err is None

    def is_err(self) -> bool:
        return self._err is not None

    def unwrap(self) -> T:
        if self.is_err():
            raise Exception(f"Called unwrap on an error: {self._err}")
        assert self._ok != None
        return self._ok

    def unwrap_err(self) -> E:
        if self.is_ok():
            raise Exception(f"Called unwrap_err on a success: {self._ok}")
        assert self._err != None
        return self._err

    def map(self, func: Callable[[T], U]) -> "Result[U, E]":
        if self.is_ok():
            assert self._ok != None
            return Result.new_ok(func(self._ok))
        else:
            return Result.new_err(self._err)

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Ok({self._ok})"
        return f"Err({self._err})"
