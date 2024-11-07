# from numpy import zeros, array, dot, tensordot
# import numpy.typing as npt
from typing import Callable
import sympy as sp
from argparse import ArgumentParser


def doArgs():
    parser = ArgumentParser(description="Matrix Multiplication Examples",)
    parser.add_argument('-n', '--number', dest='n', type=int, required=True,
                        help='example number')

    return parser.parse_args()


def tensor(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    m = sp.tensorproduct(x, y)
    sp.pprint(m)
    return sp.tensorproduct(x, y)


def dot(x: sp.Matrix, y: sp.Matrix) -> float:
    return x.dot(y)


def make_left_operator(m: sp.Matrix) -> Callable[[sp.Matrix], sp.Matrix]:
    def prod(v: sp.Matrix) -> sp.Matrix:
        return m * v
    return prod


def make_right_operator(m: sp.Matrix) -> Callable[[sp.Matrix], sp.Matrix]:
    def prod(v: sp.Matrix) -> sp.Matrix:
        return v * m
    return prod


X = sp.Matrix([
    [1, 2, 1],
    [3, 4, 3]
])
Y = sp.Matrix([
    [5, 6],
    [7, 8],
    [3, 4]
])
sX, sY, sZ = sp.symbols('X,Y,Z')


def example1():
    Z = sp.zeros(2, 2)
    for j, i in [[0, 0], [1, 0], [0, 1], [1, 1]]:
        Z[j, i] = X[j, :] * Y[:, i]

    sp.pprint(sp.Eq(sZ, Z, evaluate=False))


def example2():
    mats = [X[:, i] * Y[i, :] for i in [0, 1, 2]]
    Z = sum(mats, sp.zeros(2, 2))

    sp.pprint(sp.Eq(sZ, (sp.Eq(sp.MatAdd(*mats), Z))))


def example3():
    print("There is no code for example 3")
    pass


def example4():
    left_op = make_left_operator(X)
    Z = sp.zeros(2, 2)
    for i in [0, 1]:
        Z[:, i] = left_op(Y[:, i])

    sp.pprint(sp.Eq(sZ, Z, evaluate=False))


def example5():
    right_op = make_right_operator(Y)
    Z = sp.zeros(2, 2)
    for j in [0, 1]:
        Z[j, :] = right_op(X[j, :])

    sp.pprint(sp.Eq(sZ, Z, evaluate=False))


def main():
    args = doArgs()
    examples = [example1, example2, example3, example4, example5]

    if args.n > 0 and args.n < 1 + len(examples):
        examples[args.n - 1]()


if __name__ == "__main__":
    main()
