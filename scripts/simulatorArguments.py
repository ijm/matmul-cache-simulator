from argparse import ArgumentParser


class ArgIntTuple(object):
    def __init__(self):
        pass

    def __call__(self, s):
        return tuple(int(x) for x in s.split(","))


def doArgs():
    parser = ArgumentParser(description="Plot hilbert")
    parser.add_argument('-c', '--caches', dest='caches', nargs='+',
                        type=ArgIntTuple(), required=True, help='Caches (bits,number)')

    parser.add_argument('-l', '--link', dest='links', nargs='+', default=[],
                        type=ArgIntTuple(), help='Cache links (i.e. (0,1) => L0->L1)')

    parser.add_argument('-i', '--ifactors', dest='ifactors', nargs='+', type=int, required=True,
                        help='I factors')

    parser.add_argument('-j', '--jfactors', dest='jfactors', nargs='+', type=int, required=True,
                        help='J factors')

    parser.add_argument('-k', '--kfactors', dest='kfactors', nargs='+', type=int, required=True,
                        help='K factors')

    parser.add_argument('-f', '--filename', dest='filename', required=True,
                        help='Base file name')

    parser.add_argument('-ord', '--order', dest='order', required=True,
                        help='Caches')

    return parser.parse_args()


def tests():
    args = doArgs()
    print(f"{args=}")


if __name__ == "__main__":
    tests()
