import matplotlib as mpl
import importlib

def use_pgf() -> None:
    mpl.use('pgf')
    pgf_with_pdflatex = {
        "pgf.texsystem": "pdflatex",
        "pgf.preamble": "\n".join([
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
        ])
    }
    mpl.rcParams.update({'font.size': 9, "font.family": "serif", })
    mpl.rcParams.update(pgf_with_pdflatex)

    global plt
    plt = importlib.import_module("matplotlib.pyplot", package=None)


def use_agg() -> None:
    mpl.use('agg')

    global plt
    plt = importlib.import_module("matplotlib.pyplot", package=None)


class PltModError:
    def subplots(*_unused_args, **_unused_kwargs):
        raise AssertionError("Back end must be set first!")


plt = PltModError()


# import matplotlib.pyplot as plt  # noqa: E402
# sig:   matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)

def subplots(num_cols, num_rows, squeeze=False, **fig_kw):
    """
    Pass through of matplotlib.subplots() using the set backend, and
    squeeze defaulting to false
    """
    return plt.subplots(num_rows, num_cols, squeeze=squeeze, **fig_kw)


def savefig(fig, name: str, extensions: list[str]):
    for ex in extensions:
        # fig.savefig(".".join([name, ex]), bbox_inches='tight', dpi=200)
        fig.savefig(".".join([name, ex]), dpi=200)


def close(fig):
    plt.close(fig)


