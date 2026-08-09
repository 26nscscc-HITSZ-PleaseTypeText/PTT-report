# -*- coding: utf-8 -*-
"""Render myCPU architecture overview PNG for the design report."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent / "mycpu_arch.png"

# Prefer Windows CJK fonts so Chinese labels render
_font_candidates = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]
for _fp in _font_candidates:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
        _name = font_manager.FontProperties(fname=_fp).get_name()
        plt.rcParams["font.family"] = _name
        plt.rcParams["axes.unicode_minus"] = False
        break

fig, ax = plt.subplots(figsize=(15.5, 10.2), dpi=160)
ax.set_xlim(0, 155)
ax.set_ylim(0, 102)
ax.axis("off")
fig.patch.set_facecolor("white")


def box(x, y, w, h, text, fc, ec, fs=8, fw="bold", radius=0.4, va="center"):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.15,rounding_size={radius}",
        linewidth=1.2, facecolor=fc, edgecolor=ec,
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va=va,
            fontsize=fs, fontweight=fw, color="#222222",
            linespacing=1.25, wrap=False)
    return (x, y, w, h)


def frame(x, y, w, h, title, ec="#666666"):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        linewidth=1.4, facecolor="#f7f7f7", edgecolor=ec,
    )
    ax.add_patch(p)
    ax.text(x + 1.2, y + h - 2.2, title, ha="left", va="top",
            fontsize=11, fontweight="bold", color="#333333")


def arrow(x1, y1, x2, y2, color="#555555", style="-|>", lw=1.1, ls="-"):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                        linestyle=ls, shrinkA=2, shrinkB=2),
    )


# Outer dashed
outer = FancyBboxPatch(
    (2, 3), 151, 96,
    boxstyle="round,pad=0.3,rounding_size=0.8",
    linewidth=1.5, facecolor="none", edgecolor="#777777", linestyle=(0, (6, 4)),
)
ax.add_patch(outer)
ax.text(4, 96.5, "myCPU  ·  乱序双发射 / OOO Dual-Issue", fontsize=13,
        fontweight="bold", color="#444444", va="center")

# Colors matching reference-ish palette
C_GREEN = "#d5e8d4"
E_GREEN = "#82b366"
C_PURPLE = "#e1d5e7"
E_PURPLE = "#9673a6"
C_BLUE = "#dae8fc"
E_BLUE = "#6c8ebf"
C_RED = "#f8cecc"
E_RED = "#b85450"
C_ORANGE = "#ffe6cc"
E_ORANGE = "#d79b00"
C_YELLOW = "#fff2cc"
E_YELLOW = "#d6b656"
C_WHITE = "#ffffff"

# ===== Frontend =====
frame(4, 48, 48, 46, "前端 Frontend")
box(7, 80, 42, 10, "Branch Predict Unit  分支预测\nFTB | TAGE | RAS | uBTB | fallback BTB",
    C_GREEN, E_GREEN, fs=7.5)
box(7, 70, 42, 7, "FTQ  Fetch Target Queue (16)", C_PURPLE, E_PURPLE, fs=8)
box(7, 59, 42, 8, "IFU  Instruction Fetch\nPRE / IF + 预译码", C_BLUE, E_BLUE, fs=8)
box(7, 51, 42, 6, "Predecoder  预译码重定向", C_RED, E_RED, fs=8)
ax.text(28, 49.2, "取指宽度 Fetch Width = 4", ha="center", fontsize=7, color="#666666")

# ===== Backend =====
frame(55, 48, 95, 46, "后端 Backend（2 宽乱序）")
box(58, 82, 16, 8, "IB (16)\n4in/2out", C_PURPLE, E_PURPLE, fs=7.5)
box(77, 82, 14, 8, "Decoder\n×2", C_BLUE, E_BLUE, fs=7.5)
box(94, 82, 18, 8, "Rename/RAT\nROB编号重命名", C_GREEN, E_GREEN, fs=7)
box(115, 82, 12, 8, "Dispatch\n分发", C_YELLOW, E_YELLOW, fs=7.5)
box(132, 74, 14, 16, "ROB\n32\n奇偶双体", C_BLUE, E_BLUE, fs=8)

# RS
rs = FancyBboxPatch((58, 64), 70, 14, boxstyle="round,pad=0.15,rounding_size=0.4",
                    linewidth=1.2, facecolor=C_PURPLE, edgecolor=E_PURPLE)
ax.add_patch(rs)
ax.text(93, 76.2, "异构保留站 Reservation Stations", ha="center", fontsize=7.5,
        fontweight="bold", color="#333333")
box(61, 65.5, 15, 7, "RS_ALU0\n4·OOO", C_WHITE, E_PURPLE, fs=7)
box(78, 65.5, 15, 7, "RS_ALU1\n4·OOO", C_WHITE, E_PURPLE, fs=7)
box(95, 65.5, 15, 7, "RS_MEM\n4·FIFO", C_WHITE, E_PURPLE, fs=7)
box(112, 65.5, 14, 7, "RS_MDU\n2·FIFO", C_WHITE, E_PURPLE, fs=7)

# Execute
ex = FancyBboxPatch((58, 51), 70, 11, boxstyle="round,pad=0.15,rounding_size=0.4",
                    linewidth=1.2, facecolor=C_GREEN, edgecolor=E_GREEN)
ax.add_patch(ex)
ax.text(93, 60.5, "Execute 执行单元", ha="center", fontsize=7.5, fontweight="bold")
box(61, 52, 15, 6.5, "ALU0+Br", C_WHITE, E_GREEN, fs=7)
box(78, 52, 15, 6.5, "ALU1", C_WHITE, E_GREEN, fs=7)
box(95, 52, 15, 6.5, "LSU/STQ", C_WHITE, E_GREEN, fs=7)
box(112, 52, 14, 6.5, "MDU", C_WHITE, E_GREEN, fs=7)

box(132, 51, 14, 11, "Commit×2\nctrl冲刷", C_RED, E_RED, fs=7.5)
box(148, 51, 0.1, 0.1, "", C_WHITE, C_WHITE, fs=1)  # noop spacer
box(132, 63.5, 14, 8, "ARF\n4R2W", C_BLUE, E_BLUE, fs=7.5)

ax.text(100, 49.2, "Flush/Redirect: Commit -> ctrl -> Frontend (提交级单一恢复点)",
        ha="center", fontsize=7.5, color=E_RED, fontweight="bold")

# ===== Memory =====
frame(4, 6, 146, 38, "存储与地址翻译 Memory / MMU")
box(8, 28, 22, 10, "L1 ICache\n16KB 4-way VIPT", C_ORANGE, E_ORANGE, fs=7.5)
box(34, 28, 22, 10, "L1 DCache\n16KB · MSHR=2", C_ORANGE, E_ORANGE, fs=7.5)
box(60, 28, 22, 10, "STQ(16)+SB(8)\n推测写/提交写", C_RED, E_RED, fs=7.5)
box(86, 28, 28, 10, "Unified L2 128KB\n2×2048×32B 写回", C_ORANGE, E_ORANGE, fs=7.5)
box(118, 28, 26, 10, "MMU / TLB\n32 + μTLB 8/8", C_GREEN, E_GREEN, fs=7.5)

box(8, 14, 28, 9, "axi_line_bridge\n行突发 <-> AXI4 -> DDR", C_BLUE, E_BLUE, fs=7.5)

ax.text(78, 11, "IFU-I$ · LSU-D$/STQ/SB · I$/D$-L2-AXI · I$/D$-MMU (vaddr->paddr)",
        ha="center", fontsize=7.5, color="#555555")
ax.text(78, 7.5,
        "图例：绿=预测/执行  紫=队列  蓝=译码/ROB/ARF  橙=Cache  红=提交/冲刷/STQ",
        ha="center", fontsize=7, color="#777777")

# Flow arrows (simplified main path)
arrow(28, 80, 28, 77.2, E_GREEN)
arrow(28, 70, 28, 67.2, E_PURPLE)
arrow(28, 59, 28, 57.2, E_BLUE)
arrow(49, 54, 58, 85.5, "#333333", lw=1.3)  # predec -> IB
arrow(74, 86, 77, 86, E_PURPLE)
arrow(91, 86, 94, 86, E_BLUE)
arrow(112, 86, 115, 86, E_GREEN)
arrow(127, 86, 132, 86, E_YELLOW)
arrow(121, 82, 121, 78, E_PURPLE)  # dispatch down to RS area conceptually
arrow(93, 64, 93, 62.2, E_PURPLE)
arrow(139, 74, 139, 62.2, E_BLUE)  # ROB to commit
arrow(139, 62.8, 139, 71.5, E_RED, style="<|-")  # commit up note - skip messy

# Memory links
arrow(28, 51, 19, 38.2, E_ORANGE, ls="--", lw=1.0)
arrow(102.5, 52, 45, 38.2, E_ORANGE, ls="--", lw=1.0)
arrow(56, 33, 86, 33, E_ORANGE)
arrow(114, 33, 118, 33, E_ORANGE)
arrow(100, 28, 22, 23, E_BLUE, ls="--", lw=1.0)

plt.tight_layout(pad=0.4)
fig.savefig(OUT, dpi=160, bbox_inches="tight", facecolor="white")
print("Wrote", OUT, "size", OUT.stat().st_size)
