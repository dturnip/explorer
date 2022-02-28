import pytest
from explorer.lib.singleton import singleton


@singleton
class Square:
    def __init__(self, w: int) -> None:
        self.w = w

    def area(self) -> int:
        return self.w**2


@pytest.fixture
def squares() -> list[Square]:
    return [Square(2), Square(3)]


def test_singleton_memory_location(squares: list[Square]) -> None:
    a, b = squares

    assert a.area() == b.area() == 4


def test_singleton_update(squares: list[Square]) -> None:
    a, b = squares
    a.w = 4
    b.w = 5
    assert a.w == 5
