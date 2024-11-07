import numpy as np
import plotConfig as pltcfg
import sys


def setup():
    pltcfg.use_agg()


def highlight_cell(ax, xo, yo, x, y, **kwargs):
    rect = pltcfg.plt.Rectangle((xo + x - .45, yo + y - .45), 0.9, 0.9,
                                fill=False, color='red', alpha=0.66, linewidth=0.66, **kwargs)
    ax.add_patch(rect)
    return rect


#  def plotZ_XYage(i, agesL0, N0, agesL1, N1, agesL2, N2):
def plotZ_XYage(filename, i, data):
    """
    L0, N0 = data[0]
    L1, N1 = data[1]
    L2, N2 = data[2]

    X0, Y0, Z0 = L0
    X1, Y1, Z1 = L1
    X2, Y2, Z2 = L2

    """

    Xall = np.zeros((*data[0][0][0].shape, 3))
    Yall = np.zeros((*data[0][0][1].shape, 3))
    Zall = np.zeros((*data[0][0][2].shape, 3))

    for n in range(len(data)):
        r = data[n][1] + 1
        Xall[:, :, n] = (data[n][0][0] + 1) / r
        Yall[:, :, n] = (data[n][0][1] + 1) / r
        Zall[:, :, n] = (data[n][0][2] + 1) / r

    """
    Xall[:, :, 1] = data[1][0][0]
    Yall[:, :, 1] = data[1][0][1]
    Zall[:, :, 1] = data[1][0][2]

    Xall[:, :, 2] = data[2][0][0]
    Yall[:, :, 2] = data[2][0][1]
    Zall[:, :, 2] = data[2][0][2]

    Xall = np.zeros((X0.shape[0], X0.shape[1], 3))
    Xall[:, :, 0] = (X0 + 1) / (N0 + 1)
    Xall[:, :, 1] = (X1 + 1) / (N1 + 1)
    Xall[:, :, 2] = (X2 + 1) / (N2 + 1)

    Yall = np.zeros((Y0.shape[0], Y0.shape[1], 3))
    Yall[:, :, 0] = (Y0 + 1) / (N0 + 1)
    Yall[:, :, 1] = (Y1 + 1) / (N1 + 1)
    Yall[:, :, 2] = (Y2 + 1) / (N2 + 1)

    Zall = np.zeros((Z0.shape[0], Z0.shape[1], 3))
    Zall[:, :, 0] = (Z0 + 1) / (N0 + 1)
    Zall[:, :, 1] = (Z1 + 1) / (N1 + 1)
    Zall[:, :, 2] = (Z2 + 1) / (N2 + 1)

    """

    fig, axgrid = pltcfg.subplots(3, 1)

    # ----
    nr, nc, _ = Zall.shape
    ro = (16 - nr) // 2
    co = (16 - nc) // 2
    axgrid[0, 0].imshow(Zall, aspect='equal', interpolation='nearest',
                        extent=[co - 0.5, co + nc * 1 - 0.5, ro + nr * 1 - 0.5, ro - 0.5])

    Xs, Ys = np.meshgrid(range(Zall.shape[1]), range(Zall.shape[0]))
    for x, y in zip(Xs.flat, Ys.flat):
        if Zall[y, x, 0] > 0:
            highlight_cell(axgrid[0, 0], co, ro, x, y)

    # ----
    nr, nc, _ = Xall.shape
    ro = (16 - nr) // 2
    co = (16 - nc) // 2
    axgrid[0, 1].imshow(Xall, cmap='grey', aspect='equal', interpolation='nearest',
                        extent=[co - 0.5, co + nc * 1 - 0.5, ro + nr * 1 - 0.5, ro - 0.5])
    Xs, Ys = np.meshgrid(range(Xall.shape[1]), range(Xall.shape[0]))
    for x, y in zip(Xs.flat, Ys.flat):
        if Xall[y, x, 0] > 0:
            highlight_cell(axgrid[0, 1], co, ro, x, y)

    # ----
    nr, nc, _ = Yall.shape
    ro = (16 - nr) // 2
    co = (16 - nc) // 2
    axgrid[0, 2].imshow(Yall, cmap='grey', aspect='equal', interpolation='nearest',
                        extent=[co - 0.5, co + nc * 1 - 0.5, ro + nr * 1 - 0.5, ro - 0.5])
    Xs, Ys = np.meshgrid(range(Yall.shape[1]), range(Yall.shape[0]))
    for x, y in zip(Xs.flat, Ys.flat):
        if Yall[y, x, 0] > 0:
            highlight_cell(axgrid[0, 2], co, ro, x, y)

    # ---
    for j in range(3):
        axgrid[0, j].tick_params(
            top=False,
            bottom=False,
            left=False,
            right=False,
            labelleft=False,
            labelbottom=False
        )
        axgrid[0, j].set_xlim(-0.5, 16 - 0.5)
        axgrid[0, j].set_ylim(16 - 0.5, -0.5)
        axgrid[0, j].grid(alpha=0.2)
        axgrid[0, j].xaxis.set_visible(False)
        axgrid[0, j].yaxis.set_visible(False)
        axgrid[0, j].set_axis_off()

    axgrid[0, 0].set_title("Z", y=-0.02)
    # axgrid[0, 0].set_title("=", loc='right', y=-0.1)
    axgrid[0, 1].set_title("X", y=-0.02)
    # axgrid[0, 1].set_title("×", loc='right', y=-0.1)
    axgrid[0, 2].set_title("Y", y=-0.02)

    fig.set_size_inches(6, 2)
    fig.subplots_adjust(left=0.01, right=0.99, top=1.0, bottom=0.0)

    pltcfg.savefig(fig, f"{filename}-{i:04}", ["png"])
    pltcfg.close(fig)
    # sys.exit()

def plotZ_XYlines(i, linesL0, N0, linesL1, N1, linesL2, N2):
    X0, Y0, Z0 = linesL0
    X1, Y1, Z1 = linesL1
    X2, Y2, Z2 = linesL2

    ic= 0

    Xall = np.zeros((X0.shape[0], X0.shape[1], 3))
    Xall[:, :, 0] = (X0 + 1) / (N0 + 1)
    Xall[:, :, 1] = (X1 + 1) / (N1 + 1)
    Xall[:, :, 2] = (X2 + 1) / (N2 + 1)

    Yall = np.zeros((Y0.shape[0], Y0.shape[1], 3))
    Yall[:, :, 0] = (Y0 + 1) / (N0 + 1)
    Yall[:, :, 1] = (Y1 + 1) / (N1 + 1)
    Yall[:, :, 2] = (Y2 + 1) / (N2 + 1)

    Zall = np.zeros((Z0.shape[0], Z0.shape[1], 3))
    Zall[:, :, 0] = (Z0 + 1) / (N0 + 1)
    Zall[:, :, 1] = (Z1 + 1) / (N1 + 1)
    Zall[:, :, 2] = (Z2 + 1) / (N2 + 1)

    fig, axgrid = pltcfg.subplots(3, 1)

    axgrid[0, 0].imshow(Zall[:, :, ic], cmap='jet', aspect='equal', interpolation='nearest')
    axgrid[0, 1].imshow(Xall[:, :, ic], cmap='jet', aspect='equal', interpolation='nearest')
    axgrid[0, 2].imshow(Yall[:, :, ic], cmap='jet', aspect='equal', interpolation='nearest')

    for j in range(3):
        axgrid[0, j].tick_params(
            top=False,
            bottom=False,
            left=False,
            right=False,
            labelleft=False,
            labelbottom=False
        )
        axgrid[0, j].grid(alpha=0.2)
        axgrid[0, j].xaxis.set_visible(False)
        axgrid[0, j].yaxis.set_visible(False)

    axgrid[0, 0].set_title("Z")
    axgrid[0, 1].set_title("X")
    axgrid[0, 2].set_title("Y")

    fig.set_size_inches(6, 2)

    pltcfg.savefig(fig, f"out-{i:04}", ["png"])
    close(fig)



max0 = 1
max1 = 1
max2 = 1
a = 0.8


def plotBar(i, hlen, cntHistory):
    fig, axgrid = pltcfg.subplots(3, 1)
    b = np.array(cntHistory)

    axgrid[0, 0].plot(b[:, 0, 0], b[:, 0, 1])
    axgrid[0, 0].plot(b[:, 0, 0], b[:, 0, 2])
    axgrid[0, 0].plot(b[:, 0, 0], b[:, 0, 3])

    global max0
    max0 = max0 * (1 - a) + a * max(max0, b[:, 0, 1:].max())
    axgrid[0, 0].set_ylim((0, max0 * 1.05))
    axgrid[0, 0].set_xlim((i - hlen, i))
    axgrid[0, 0].set_box_aspect(1)

    axgrid[0, 1].bar(b[:, 1, 0], b[:, 1, 1], width=0.8)
    axgrid[0, 1].bar(b[:, 1, 0], b[:, 1, 2], width=0.8)
    axgrid[0, 1].bar(b[:, 1, 0], b[:, 1, 3], width=0.8)

    global max1
    max1 = max1 * (1 - a) + a * max(max1, b[:, 1, 1:].max())
    axgrid[0, 1].set_ylim((0, max1 * 1.05))
    axgrid[0, 1].set_xlim((i - hlen, i))
    axgrid[0, 1].set_box_aspect(1)

    axgrid[0, 2].plot(b[:, 2, 0], b[:, 2, 1])
    axgrid[0, 2].plot(b[:, 2, 0], b[:, 2, 2])
    axgrid[0, 2].plot(b[:, 2, 0], b[:, 2, 3])

    global max2
    max2 = max2 * (1 - a) + a * max(max2, b[:, 2, 1:].max())
    axgrid[0, 2].set_ylim((0, max2 * 1.05))
    axgrid[0, 2].set_xlim((i - hlen, i))
    axgrid[0, 2].set_box_aspect(1)

    fig.set_size_inches(6, 2)
    fig.subplots_adjust(wspace=0.3, hspace=0.2)
    pltcfg.savefig(fig, f"out-{i:04}", ["png"])
    close(fig)




if __name__ == "__main__":
    main()
