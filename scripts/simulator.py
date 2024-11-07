# form argparse import ArgumentParser, FileType
# from sys import stdout
import numpy as np
import functools as ft
import itertools as it

# from typing import Iterable, Callable
from typing_extensions import Self
from dataclasses import dataclass
from copy import deepcopy
from math import prod

from cache import Cache, CmdLogger, ACCESS, MemoryInterface, VMatrix
from indexer import Indexer
import plots
from simulatorArguments import doArgs
import sys

plots.setup()


def accessesFromIndicies(memoryInterface, indexes):
    i, j, k = indexes
    matX, matY, matZ = memoryInterface.blocks
    # print(f"{indexes=}")
    # Z[j, i] += X[j, k] * Y[k, i]

    accesses = [
        (matX.location(j, k), ACCESS.READ),
        (matY.location(k, i), ACCESS.READ),
        (matZ.location(j, i), ACCESS.WRITE),
    ]
    return accesses


def render(memory, cmds, mapfunc, plotfunc, filename):
    for i, _ in enumerate(cmds):
        if i % 100 == 0:
            print(i)
        data = [(mapfunc(c), c.numlines) for c in memory.cache_top]
        plotfunc(filename, i, data)


def main():
    args = doArgs()

    # Setup Indexing. note tile sizes also set matrix sizes
    ijkFactors = [args.ifactors, args.jfactors, args.kfactors]
    indexer = Indexer(ijkFactors, args.order)

    i_max, j_max, k_max = indexer.maxes

    # Set up Caches.
    cmd_logger = CmdLogger()

    caches = [Cache(ident=i, lineBits=lb, numlines=n, cmd_logger=cmd_logger)
              for i, (lb, n) in enumerate(args.caches)]

    for a, b in args.links:
        caches[a].set_next_cache(caches[b])

    # Setup Memory.
    matX = VMatrix(ident=0, width=k_max, height=j_max)
    matY = VMatrix(ident=0, width=i_max, height=k_max)
    matZ = VMatrix(ident=0, width=i_max, height=j_max)
    matricies = [matX, matY, matZ]

    # Setup Memory Interface.
    memory = MemoryInterface(cmd_logger, caches[0], matricies)

    print(indexer)
    print(memory)

    # Setup Pipeline. range->indicies->mem accesses->cache cmds->cache states->viz

    getInd = ft.partial(accessesFromIndicies, memory)

    total_iterations = prod(indexer.maxes)
    print(f"{total_iterations=}")

    inx = range(total_iterations)
    indicies = map(indexer.indiciesOfIndex, inx)
    accesses = map(getInd, indicies)
    cmds = map(memory.cmdsFromAccesses, accesses)

    if True:
        render(memory, cmds, memory.agesFromState, plots.plotZ_XYage, args.filename)

    if False:
        render(memory, cmds, memory.linesFromState, plots.plotZ_XYlines, args.filename)

    """
        for i, _ in enumerate(cmds):
            if i % 100 == 0:
                print(i)
            linesL0 = memory.linesFromState(cacheL0)
            linesL1 = memory.linesFromState(cacheL1)
            linesL2 = memory.linesFromState(cacheL2)
            plots.plotZ_XYlines(
                i,
                linesL0, cacheL0.numlines,
                linesL1, cacheL1.numlines,
                linesL2, cacheL2.numlines
            )
    """


    def countCmds(cmds):
        NCaches = 3
        NCmds = 4  # cmd 0 doesn't exist
        cnts = np.zeros((NCaches, NCmds))

        for c in cmds:
            (ident, cmd, _unused_line, _unused_lineLoc) = c
            cnts[ident, cmd.value] += 1

        return cnts

    if False:
        accessPerFrame = 20
        historyLength = 40

        cnthistory = []

        for i, batch in enumerate(it.batched(cmds, accessPerFrame)):
            if i % 100 == 0:
                print(i)
            counts = countCmds(it.chain(*batch))
            counts[:, 0] = i
            cnthistory = cnthistory[-historyLength + 1:]
            cnthistory.append(counts)
            plots.plotBar(i, historyLength, cnthistory)

    if False:
        print(list(cmds))
        cmd_logger.clear()
        caches[0].evict_all()
        cmds = cmd_logger.get()
        print(list(cmds))


if __name__ == "__main__":
    main()
