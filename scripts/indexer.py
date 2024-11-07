# from typing import Iterable, Callable
from typing_extensions import Self
from copy import deepcopy
from math import prod


class Indexer():
    IJKList = tuple[list[int], list[int], list[int]]
    IJK = tuple[int, int, int]
    ordering: str
    ijkBases: IJKList
    basesIn: list[int]
    derefs: IJKList
    maxes: IJK

    def __init__(self: Self, ijkBases: IJKList, ordering: str):
        self.ijkBases = ijkBases
        self.ordering = ordering

        ijkCopy = deepcopy(ijkBases)
        self.basesIn = [ijkCopy[ord(c) - ord('i')].pop(0) for c in ordering]

        derefs = [[], [], []]
        for x, c in enumerate(ordering[::-1]):
            derefs[ord(c) - ord('i')].append(x)
        for x in derefs:
            x.reverse()
        self.derefs = derefs

        self.maxes = [prod(x) for x in ijkBases]

    def __str__(self: Self) -> str:
        return f"Indexer<ordering={self.ordering} ijk_factors={self.ijkBases} ijk_maxes={self.maxes}>"

    def indiciesOfIndex(self: Self, index: int) -> IJK:
        def digitsOfInt(n: int, bases: list[int]):
            digits = []
            for base in bases[::-1]:
                digits.append(n % base)
                n = n // base
            return digits  # [::-1]

        def intOfDigits(digits: list[int], bases: list[int]) -> int:
            # if len(digits) != len(bases):
            #     raise ValueError("Digits and bases don't line up")
            num = 0
            for b, v in zip(bases[:], digits[:]):
                num = num * b + v
            return num

        digits = digitsOfInt(index, self.basesIn)
        ds = [[digits[r] for r in refs] for refs in self.derefs]
        iis = [intOfDigits(d, b) for d, b in zip(ds, self.ijkBases)]
        # print(f"{index=} {digits=} {ds=} {iis=} {self.derefs=} {self.ijkBases=}")
        return iis


def tests():
    raise NotImplementedError("TBD")


if __name__ == "__main__":
    tests()
