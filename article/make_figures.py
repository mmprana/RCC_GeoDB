"""
Generate the six manuscript figures as high-resolution PNGs.

Run with:
    /tmp/opencode/venv/bin/python make_figures.py
"""

import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# Palette
BLUE = "#2E5E8C"
LIGHT_BLUE = "#DCE9F5"
GREEN = "#2E7D5B"
LIGHT_GREEN = "#E2F0E8"
ORANGE = "#C55A11"
LIGHT_ORANGE = "#FBE5D6"
RED = "#A61C1C"
LIGHT_RED = "#F4CCCC"
GRAY = "#555555"
LIGHT_GRAY = "#F2F2F2"
WHITE = "#FFFFFF"
DARK = "#222222"


def setup_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)
    return fig, ax


def draw_box(ax, x, y, w, h, text, fc, ec, fontsize=10, bold=False, wrap=24):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.4,rounding_size=1.2",
        linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=2
    )
    ax.add_patch(box)
    label = "\n".join(textwrap.fill(part, width=wrap) for part in str(text).split("\n"))
    ax.text(
        x, y, label, ha="center", va="center",
        fontsize=fontsize, color=DARK,
        fontweight="bold" if bold else "normal",
        zorder=3, linespacing=1.25
    )


def arrow(ax, x1, y1, x2, y2, color=GRAY, style="-|>", lw=1.6, linestyle="-"):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=14,
        linewidth=lw, color=color, linestyle=linestyle, zorder=1
    )
    ax.add_patch(arr)


def label(ax, x, y, text, fontsize=9, color=GRAY, ha="center", va="center", italic=True):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize, color=color, style="italic" if italic else "normal")


def fig1_workflow():
    fig, ax = setup_axes((13, 7.5))
    ax.text(24, 96, "(a) Current paper/Excel workflow", ha="center", fontsize=12, fontweight="bold", color=RED)
    ax.text(76, 96, "(b) Proposed staged digital workflow", ha="center", fontsize=12, fontweight="bold", color=GREEN)

    # Current
    xs = 24
    ys = [82, 64, 46, 28]
    texts = [
        "Paper maps, Excel registers, CAD files, departmental memory",
        "Departmental files and informal coordination",
        "Duplication, inconsistency, and slow handovers",
        "Slow reporting and weak accountability",
    ]
    for i, (y, t) in enumerate(zip(ys, texts)):
        draw_box(ax, xs, y, 38, 12, t, LIGHT_RED, RED, fontsize=9, wrap=32)
        if i < len(ys) - 1:
            arrow(ax, xs, y - 6, xs, ys[i + 1] + 6, color=RED)

    # Proposed
    xs2 = 76
    ys2 = [86, 73, 60, 47, 34, 21]
    texts2 = [
        "Capture: QGIS, QField, Excel templates, CAD, paper maps",
        "Stage: load metadata, source, accuracy",
        "Validate: CRS, domains, geometry, keys",
        "Production geodatabase: PostGIS or file geodatabase",
        "Use and share: QGIS, internal Lizmap, public views",
        "Feedback: corrections, audits, maintenance",
    ]
    for i, (y, t) in enumerate(zip(ys2, texts2)):
        draw_box(ax, xs2, y, 38, 9.5, t, LIGHT_GREEN, GREEN, fontsize=8.5, wrap=34)
        if i < len(ys2) - 1:
            arrow(ax, xs2, y - 4.75, xs2, ys2[i + 1] + 4.75, color=GREEN)

    # Feedback loop
    ax.plot([95, 98, 98, 95], [21, 21, 86, 86], color=GREEN, linewidth=1.2, linestyle="--", zorder=1)
    arrow(ax, 98, 86, 95, 86, color=GREEN, linestyle="--")

    fig.savefig(os.path.join(FIGDIR, "fig1_workflow.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def fig2_architecture():
    fig, ax = setup_axes((14, 9))
    ax.text(12, 96, "Sources", ha="center", fontsize=12, fontweight="bold", color=ORANGE)
    ax.text(50, 96, "Data platform", ha="center", fontsize=12, fontweight="bold", color=BLUE)
    ax.text(87, 96, "Users and publication", ha="center", fontsize=12, fontweight="bold", color=GREEN)

    sources = [
        ("Paper maps and scans", 82),
        ("Excel and CSV", 68),
        ("CAD and engineering drawings", 54),
        ("QField field capture", 40),
        ("Partner agency data", 26),
    ]
    for text, y in sources:
        draw_box(ax, 12, y, 20, 9, text, LIGHT_ORANGE, ORANGE, fontsize=8.5, wrap=20)

    draw_box(ax, 50, 82, 22, 9, "Staging schema\n(load ID, source, accuracy)", LIGHT_BLUE, BLUE, fontsize=8.5, wrap=22)
    draw_box(ax, 50, 66, 22, 9, "Validation and QA\n(CRS, domains, geometry, keys)", LIGHT_BLUE, BLUE, fontsize=8.5, wrap=22)
    draw_box(ax, 50, 46, 24, 12, "Production geodatabase\nPostGIS or file geodatabase", "#D6E4F0", BLUE, fontsize=9, bold=True, wrap=24)
    draw_box(ax, 50, 27, 22, 8, "Metadata catalogue\nlayers, fields, domains", LIGHT_GRAY, GRAY, fontsize=8.5, wrap=22)
    draw_box(ax, 50, 13, 22, 8, "Audit and history\nwho changed what, when", LIGHT_GRAY, GRAY, fontsize=8.5, wrap=22)

    users = [
        ("QGIS Desktop\nediting and analysis", 82, LIGHT_GREEN, GREEN),
        ("QGIS Server + Lizmap\ninternal map", 66, LIGHT_GREEN, GREEN),
        ("Public views and APIs\nselective layers", 50, LIGHT_GREEN, GREEN),
        ("QField\nfield capture", 34, LIGHT_GREEN, GREEN),
        ("Print and reports\nward maps, asset reports", 18, LIGHT_GREEN, GREEN),
    ]
    for text, y, fc, ec in users:
        draw_box(ax, 87, y, 21, 8.5, text, fc, ec, fontsize=8.5, wrap=20)

    # Source to staging arrows
    for _, y in sources:
        arrow(ax, 22, y, 39, 82 if y > 60 else 70, color=ORANGE, lw=1.1)
    arrow(ax, 50, 77.5, 50, 70.5, color=BLUE)
    arrow(ax, 50, 61.5, 50, 52, color=BLUE)
    arrow(ax, 50, 40, 50, 31, color=GRAY, linestyle="--")
    arrow(ax, 50, 40, 50, 17, color=GRAY, linestyle="--")

    # Platform to users
    for y in (82, 66, 50, 34, 18):
        arrow(ax, 62, 46, 76.5, y, color=GREEN, lw=1.1)

    # Metadata/audit up to validation/production
    arrow(ax, 61, 27, 61, 40, color=GRAY, linestyle="--")
    arrow(ax, 61, 13, 61, 27, color=GRAY, linestyle="--")

    fig.savefig(os.path.join(FIGDIR, "fig2_architecture.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def draw_entity(ax, x, y, w, h, title, fields, fc=LIGHT_BLUE, ec=BLUE):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.35,rounding_size=1.0",
        linewidth=1.3, edgecolor=ec, facecolor=fc, zorder=2
    )
    ax.add_patch(box)
    header_h = 3.1
    header = Rectangle(
        (x - w / 2 + 0.15, y + h / 2 - header_h - 0.15),
        w - 0.3, header_h,
        facecolor=ec, edgecolor="none", alpha=0.18, zorder=3
    )
    ax.add_patch(header)
    ax.text(x, y + h / 2 - header_h / 2 - 0.15, title, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=DARK, zorder=4)
    ax.text(x, y + h / 2 - header_h - 1.4, fields, ha="center", va="top",
            fontsize=6.8, color=DARK, zorder=4, linespacing=1.25)


def rel(ax, x1, y1, x2, y2, text="1:N"):
    ax.plot([x1, x2], [y1, y2], color="#8A8A8A", linewidth=1.2, zorder=1)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my, text, fontsize=7, color=GRAY, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.15", facecolor=WHITE, edgecolor="none"), zorder=4)


def fig3_erd():
    fig, ax = setup_axes((14, 9))
    ax.text(50, 97, "Core municipal data model (simplified)", ha="center", fontsize=12, fontweight="bold", color=BLUE)

    draw_entity(ax, 50, 86, 20, 9, "WARD", "ward_code (PK)\nward_name\nthana_code")
    draw_entity(ax, 22, 65, 22, 11, "PARCEL", "parcel_id (PK)\nkhatian_no, dag_no\nward_code (FK)")
    draw_entity(ax, 78, 65, 22, 11, "ROAD", "road_id (PK)\nroad_name\nward_code (FK)")
    draw_entity(ax, 22, 42, 22, 11, "BUILDING", "building_id (PK)\nparcel_id (FK)\nholding_no")
    draw_entity(ax, 50, 42, 24, 12, "ADDRESS", "address_id (PK)\nroad_id (FK)\nbuilding_id (FK)\nparcel_id (FK)")
    draw_entity(ax, 78, 42, 22, 11, "ASSET REGISTRY", "asset_no (PK)\nasset_class\nward_code (FK)")
    draw_entity(ax, 22, 17, 22, 10, "DRAIN", "asset_no (PK)\nshape\ncondition_code")
    draw_entity(ax, 50, 17, 22, 10, "MANHOLE", "asset_no (PK)\nparent_asset_no (FK)\ninvert_level_m")
    draw_entity(ax, 78, 17, 22, 10, "WASTE BIN", "asset_no (PK)\nzone_id (FK)\nroute_id (FK)")

    rel(ax, 50, 81.5, 33, 70.5)
    rel(ax, 50, 81.5, 67, 70.5)
    rel(ax, 22, 59.5, 22, 47.5)
    rel(ax, 33, 59.5, 44, 48)
    rel(ax, 67, 59.5, 56, 48)
    rel(ax, 33, 42, 38, 42)
    rel(ax, 78, 36.5, 78, 22)
    rel(ax, 33, 22, 39, 22)

    ax.text(50, 6.5, "Note: the asset registry provides a common key across drain, manhole, bin, and other asset tables.",
            ha="center", fontsize=8, color=GRAY, style="italic")

    fig.savefig(os.path.join(FIGDIR, "fig3_erd.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def fig4_lifecycle():
    fig, ax = setup_axes((10, 10))
    ax.text(50, 97, "Data lifecycle and validation pipeline", ha="center", fontsize=12, fontweight="bold", color=BLUE)

    items = [
        ("Capture\nQGIS, QField, Excel, CAD, paper maps", 88, LIGHT_BLUE, BLUE),
        ("Stage\nload metadata, source, accuracy", 76, LIGHT_BLUE, BLUE),
        ("Validate\nCRS, domains, geometry, keys", 64, LIGHT_BLUE, BLUE),
        ("Approve\nsteward sign-off", 52, LIGHT_BLUE, BLUE),
        ("Publish\nproduction and public views", 40, LIGHT_GREEN, GREEN),
        ("Use\nplanning, operations, services", 28, LIGHT_GREEN, GREEN),
        ("Feedback\ncorrections, audits, maintenance", 16, LIGHT_GREEN, GREEN),
    ]
    for text, y, fc, ec in items:
        draw_box(ax, 48, y, 54, 8, text, fc, ec, fontsize=8.5, wrap=46)
    for i in range(len(items) - 1):
        arrow(ax, 48, items[i][1] - 4, 48, items[i + 1][1] + 4, color=BLUE if i < 3 else GREEN)

    # Feedback loop
    ax.plot([78, 88, 88, 78], [16, 16, 88, 88], color=GREEN, linewidth=1.4, linestyle="--", zorder=1)
    arrow(ax, 88, 88, 78, 88, color=GREEN, linestyle="--")

    # Fail loop
    ax.plot([18, 10, 10, 18], [64, 64, 76, 76], color=RED, linewidth=1.2, linestyle="--", zorder=1)
    arrow(ax, 10, 76, 18, 76, color=RED, linestyle="--")
    label(ax, 13, 70, "fail:\nerror report", fontsize=8, color=RED)

    fig.savefig(os.path.join(FIGDIR, "fig4_lifecycle.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def fig5_governance():
    fig, ax = setup_axes((10, 8))
    ax.text(50, 95, "Data governance framework", ha="center", fontsize=12, fontweight="bold", color=BLUE)

    items = [
        ("Principles\npublic value, stewardship, quality,\nopenness, privacy, security, equity", 81, LIGHT_BLUE, BLUE),
        ("Roles\nmayor/board, CEO, GIS unit,\ndata owners, stewards, users, public", 64, LIGHT_GREEN, GREEN),
        ("Policies\nstandards, metadata, access, privacy,\nretention, sharing, procurement", 47, LIGHT_ORANGE, ORANGE),
        ("Processes\ndata request, change request, QA,\npublication approval, incident response", 30, LIGHT_GRAY, GRAY),
        ("Evaluation\nmaturity, completeness, timeliness,\nuse, trust, public value", 13, "#E8DDF2", "#6A4C93"),
    ]
    for text, y, fc, ec in items:
        draw_box(ax, 45, y, 58, 11.5, text, fc, ec, fontsize=8.5, wrap=50)
    for i in range(len(items) - 1):
        arrow(ax, 45, items[i][1] - 5.75, 45, items[i + 1][1] + 5.75, color=GRAY)

    # Feedback loop on the right
    ax.plot([74, 84, 84, 74], [13, 13, 81, 81], color="#6A4C93", linewidth=1.4, linestyle="--", zorder=1)
    arrow(ax, 84, 81, 74, 81, color="#6A4C93", linestyle="--")
    label(ax, 88, 47, "feedback", fontsize=8, color="#6A4C93")

    fig.savefig(os.path.join(FIGDIR, "fig5_governance.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def fig6_roadmap():
    fig, ax = plt.subplots(figsize=(13, 6.5))
    fig.patch.set_facecolor(WHITE)
    phases = [
        ("0. Foundation", 0, 3, "#B4C7E7"),
        ("1. Pilot ward", 3, 3, "#A9D18E"),
        ("2. City foundation", 6, 6, "#FFD966"),
        ("3. Operations", 12, 6, "#F4B183"),
        ("4. Public", 18, 6, "#9DC3E6"),
        ("5. Scale", 24, 12, "#C5E0B4"),
    ]
    for i, (name, start, duration, color) in enumerate(phases):
        y = len(phases) - i - 1
        ax.broken_barh([(start, duration)], (y - 0.35, 0.7), facecolors=color, edgecolors="#666666", linewidth=0.8)
        ax.text(-0.5, y, name, ha="right", va="center", fontsize=10)
        ax.text(start + duration / 2, y, f"{start}-{start + duration}m", ha="center", va="center", fontsize=8, color="#333333")

    for gate, label_text in [(3, "G1"), (6, "G2"), (12, "G3"), (18, "G4"), (24, "G5")]:
        ax.plot(gate, -0.7, marker="D", markersize=8, color="#A61C1C", zorder=3)
        ax.text(gate, -1.2, label_text, ha="center", va="top", fontsize=8, color="#A61C1C")

    ax.set_xlim(0, 37)
    ax.set_ylim(-1.8, 6.0)
    ax.set_xlabel("Months from start", fontsize=10)
    ax.set_yticks([])
    ax.set_xticks([0, 3, 6, 12, 18, 24, 30, 36])
    ax.grid(axis="x", linestyle=":", color="#BBBBBB", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Phased implementation roadmap", fontsize=12, fontweight="bold", color=BLUE, loc="left")
    ax.text(36, -1.65, "G1–G5 = decision gates", fontsize=8, color=GRAY, style="italic", ha="right")

    fig.savefig(os.path.join(FIGDIR, "fig6_roadmap.png"), dpi=300, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


if __name__ == "__main__":
    fig1_workflow()
    fig2_architecture()
    fig3_erd()
    fig4_lifecycle()
    fig5_governance()
    fig6_roadmap()
    print("Figures written to", FIGDIR)
