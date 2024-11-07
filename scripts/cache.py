import numpy as np

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from typing_extensions import Self


class CState(Enum):
    EMPTY = 0
    CLEAN = 1
    DIRTY = 2


class CCmd(Enum):
    SPILL = 1
    FILL = 2
    KILL = 3


class ACCESS(Enum):
    READ = 0
    WRITE = 1


@dataclass
class CacheLine:
    state: CState = CState.EMPTY  # 0 = unused, 1 = clean, 2 = dirty
    lineLoc: int = None  # pointer to first memory associated in units of cache-lines

    def __str__(self: Self):
        return f"{self.lineLoc}{['-','+','!'][self.state]}"


class CmdLogger():
    CmdTuple = tuple[int, CCmd, int, int]
    cmds: list[CmdTuple]

    def __init__(self: Self) -> None:
        self.clear()

    def clear(self: Self) -> None:
        self.cmds = []

    def get(self: Self) -> list[CmdTuple]:
        return self.cmds

    def emit(self: Self, cmdLine: CmdTuple) -> None:
        self.cmds.append(cmdLine)


class Cache():
    lineBits: int
    numlines: int
    cmd_logger: CmdLogger
    lines: list[CacheLine]
    lineIndex: dict
    lru: list[int]
    next_cache: Self
    # cmds: list

    def __init__(self: Self, ident: int, lineBits: int, numlines: int, cmd_logger: CmdLogger):
        self.ident = ident
        self.lineBits = lineBits  # log2(linewidth)
        self.numlines = numlines
        self.cmd_logger = cmd_logger
        self.lines = [CacheLine() for _ in range(numlines)]
        self.lineIndex = {}
        self.lru = list(range(numlines))
        self.next_cache = None
        # self._cachecmds = []

    def __str__(self: Self) -> str:
        return f"Cache<{self.ident}: {self.numlines} lines of {self.lineBits} bits>"

    def __iter__(self: Self):
        while True:
            yield self
            if (self := self.next_cache) is None:
                break

    def set_next_cache(self: Self, next_cache: Self):
        self.next_cache = next_cache

    def get_next_cache(self: Self):
        yield self.next_cache

    def inCache(self: Self, location: int) -> Optional[int]:
        lineLoc = location >> self.lineBits
        return self.lineIndex.get(lineLoc)

    def age(self: Self, location: int) -> int:
        lineLoc = location >> self.lineBits
        line = self.lineIndex.get(lineLoc)
        return self.lru.index(line) if line is not None else -1

    def line(self: Self, location: int) -> int:
        lineLoc = location >> self.lineBits
        line = self.lineIndex.get(lineLoc)
        return line if line is not None else -1

    def emit(self: Self, cmd: CCmd, line: int, lineLoc: int) -> None:
        self.cmd_logger.emit((self.ident, cmd, line, lineLoc))

        if self.next_cache is not None:
            if cmd == CCmd.FILL:
                self.next_cache.access(lineLoc << self.lineBits, ACCESS.READ)
            elif cmd == CCmd.SPILL:
                self.next_cache.access(lineLoc << self.lineBits, ACCESS.WRITE)
            else:
                pass

    def assign_line(self: Self, line: int, location: int) -> None:
        if self.lines[line].state != CState.EMPTY:
            raise KeyError("Line isn't empty!")

        lineLoc = location >> self.lineBits

        if lineLoc in self.lineIndex:
            raise KeyError("Location already indexed!")

        self.lines[line].state = CState.CLEAN
        self.lines[line].lineLoc = lineLoc
        self.lineIndex[lineLoc] = line
        self.emit(CCmd.FILL, line, lineLoc)

    def evict_line(self: Self, line: int) -> None:
        if self.lines[line].state == CState.EMPTY:
            return

        lineLoc = self.lines[line].lineLoc
        if self.lineIndex.get(lineLoc) != line:
            raise KeyError("Oldest line not in index?")

        if self.lines[line].state == CState.DIRTY:
            self.emit(CCmd.SPILL, line, lineLoc)
        else:
            self.emit(CCmd.KILL, line, lineLoc)

        self.lines[line].state = CState.EMPTY
        self.lines[line].lineLoc = 0
        del self.lineIndex[lineLoc]

    def set_dirty_line(self: Self, line: int):
        if self.lines[line].state == CState.EMPTY:
            raise KeyError(f"Attempt to dirty an empty line {line=}.")
        self.lines[line].state = CState.DIRTY

    def move_to_top(self: Self, line: int) -> None:
        inx = self.lru.index(line)
        del self.lru[inx]
        self.lru.append(line)

    def evict_all(self: Self) -> None:
        for line in self.lru:
            self.evict_line(line)

    def access(self, location: int, atype: ACCESS) -> None:
        line = self.inCache(location)
        if line is None:
            line = self.lru[0]
            self.evict_line(line)
            self.assign_line(line, location)
        if atype == ACCESS.WRITE:
            self.set_dirty_line(line)
        self.move_to_top(line)


@dataclass
class VMatrix():
    ident: int
    width: int
    height: int
    rowMajor: bool = True
    offset: int = 0

    def __str__(self: Self) -> str:
        return f"VMatrix<{self.ident}: [{self.height}x{self.width}] " \
               f"{'row-major' if self.rowMajor else 'col-major'} " \
               f"@ {self.offset:04}>"

    def location(self: Self, y: int, x: int) -> int:
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise KeyError(f"{(y, x)} not inside matrix of size {(self.height, self.width)}")
        return self.offset + y * self.width + x if self.rowMajor else x * self.height + y

    def locate(self: Self, offset: int):
        self.offset = offset

    def length(self: Self):
        return self.width * self.height


class MemoryInterface():
    cmd_logger: CmdLogger
    cache_top: Cache
    blocks: list

    def __init__(self: Self, cmd_logger: CmdLogger, cache_top: Cache, blocks):
        self.cmd_logger = cmd_logger
        self.cache_top = cache_top
        self.blocks = blocks

        ptr = 0
        for blk in blocks:
            blk.locate(ptr)
            ptr += blk.length()

    def __str__(self: Self):
        return "Memory:\n  " +\
               "\n  ".join(f"{blk}" for blk in self.blocks) +\
               "\nCaches:\n  " +\
               "\n  ".join(f"{cache}" for cache in self.cache_top)

    def cmdsFromAccesses(self, accesses):
        self.cmd_logger.clear()

        for x in accesses:
            self.cache_top.access(*x)

        cmds = self.cmd_logger.get()
        return cmds

    def agesFromState(self, cache):
        def mkMesh(mat):
            return np.meshgrid(range(mat.width), range(mat.height))

        getAge = np.vectorize(lambda m, x, y: cache.age(m.location(y, x)))

        return [getAge(mat, *mkMesh(mat)) for mat in self.blocks]

    def linesFromState(self, cache):
        def mkMesh(mat):
            return np.meshgrid(range(mat.width), range(mat.height))

        getLine = np.vectorize(lambda m, x, y: cache.line(m.location(y, x)))

        return [getLine(mat, *mkMesh(mat)) for mat in self.blocks]


def tests():
    cmd_logger = CmdLogger()
    cache = Cache(0, 0, 4, cmd_logger)

    accesses = [
        (15, ACCESS.READ),
        (31, ACCESS.READ),
        (15, ACCESS.WRITE),
        (99, ACCESS.READ),
        (45, ACCESS.READ),
        (22, ACCESS.READ),
        (23, ACCESS.READ),
        (24, ACCESS.READ),
    ]

    cmds = []

    for x in accesses:
        cmd_logger.clear()
        cache.access(*x)
        cmds.append(cmd_logger.get())

    for a, c in zip(accesses, cmds):
        print(f"Memory{a} => {c}")

    cmd_logger.clear()
    cache.evict_all()
    cmds = cmd_logger.get()

    print(f"Flush: {cmds}")


if __name__ == "__main__":
    tests()
