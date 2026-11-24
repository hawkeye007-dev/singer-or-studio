"""Generate the two manuscript plots from the archived experiment results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import NullLocator

INK = "#22282d"
MUTED = "#4e5a65"
GRID = "#d9dfe4"
BLUE = "#245774"
RUST = "#a14c32"
TEAL = "#3b7166"

MODELS = [
    ("cvsm_art", "CVSM-ART", BLUE, "-", "o"),
    ("cvsm_a", "CVSM-A", TEAL, "--", "s"),
    ("ssl", "Torres SSL", RUST, "-.", "^"),
    ("ecapa", "ECAPA-TDNN", "#3c444a", ":", "D"),
    ("mert", "MERT", "#717981", (0, (4, 2, 1, 2)), "x"),
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": MUTED,
    "axes.titleweight": "bold",
    "xtick.color": INK,
    "ytick.color": INK,
    "pdf.fonttype": 42,
    "savefig.facecolor": "white",
})


def read(path):
    return json.loads(path.read_text())


def save(fig, output, name):
    fig.savefig(output / f"{name}.pdf")
    plt.close(fig)


def clean_axes(ax, axis):
    ax.spines[["right", "top"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis=axis, color=GRID, linewidth=0.55)
    ax.tick_params(length=2.5, width=0.65)


def factorial(archive, output):
    cells = read(archive / "factorial/results.json")["jvs"]["models"]["cvsm_art"]["roles"][
        "common"]["conditions"]["reverb_20"]["cells"]
    keys = ("000", "010", "011", "100")
    fig = plt.figure(figsize=(7.15, 2.42))
    grid = fig.add_gridspec(1, 3, width_ratios=(1.12, 1, 0.80),
                           left=0.02, right=0.98, bottom=0.23, top=0.80, wspace=0.33)
    layout, ax, scores = [fig.add_subplot(grid[i]) for i in range(3)]
    layout.set(xlim=(0, 3.85), ylim=(-0.6, 3.6))
    layout.axis("off")
    layout.set_title("(a) Processing by trial role", loc="left", pad=18, fontsize=9)
    ax.set_title("(b) Ranking error", loc="left", pad=18, fontsize=9)
    scores.set_title("(c) Mean cosine", loc="left", pad=18, fontsize=9)
    for x, label in zip((1.44, 2.39, 3.34), ("Query", "Genuine", "Impostor")):
        layout.text(x, 3.73, label, ha="center", va="bottom", weight="bold",
                    fontsize=7, clip_on=False)
    for y, key in zip((3, 2, 1, 0), keys):
        layout.text(0.17, y, key, va="center", family="monospace", fontsize=9)
        for x, state in zip((1.44, 2.39, 3.34), key):
            treated = state == "1"
            changed = key == "011" and x == 3.34
            layout.add_patch(Rectangle((x - 0.43, y - 0.31), 0.86, 0.62,
                                       facecolor="#e2edf3" if treated else "white",
                                       edgecolor=BLUE if changed else GRID,
                                       linewidth=1.5 if changed else 0.7,
                                       hatch="//" if changed else None))
            layout.text(x, y, "Reverb" if treated else "Dry", ha="center", va="center",
                        color=INK, weight="bold" if changed else "normal",
                        bbox={"facecolor": "#e2edf3", "edgecolor": "none", "pad": 0.8}
                        if changed else None)
    for y, key in zip((3, 2, 1, 0), keys):
        d = cells[key]["ranking_error_pct"]
        value = d["value"]
        lo, hi = d["ci95"]
        color = RUST if key == "010" else BLUE
        ax.errorbar(value, y, xerr=[[value - lo], [hi - value]], fmt="o", markersize=4.6,
                    color=color, capsize=2.5, linewidth=1)
        ax.text(hi + 1.3, y, f"{value:.2f}%", va="center", color=INK, fontsize=7.4)
    ax.set(xlim=(0, 69), ylim=(-0.6, 3.6), xticks=(0, 15, 30, 45, 60), yticks=[],
           xlabel="Ranking error (%)")
    clean_axes(ax, "x")
    ax.spines["left"].set_visible(False)
    for field, label, style, mark, color in (
        ("genuine_cosine", "Genuine", "-", "o", INK),
        ("impostor_cosine", "Impostor", "--", "s", BLUE),
    ):
        values = [cells[k][field]["value"] for k in ("010", "011")]
        scores.plot((0, 1), values, linestyle=style, marker=mark,
                    markersize=4, linewidth=1.15, color=color, label=label)
    scores.set(xlim=(-0.15, 1.15), ylim=(0.83, 0.905), xticks=(0, 1),
               xticklabels=("010", "011"), yticks=(0.84, 0.86, 0.88, 0.90))
    clean_axes(scores, "y")
    scores.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2,
                  frameon=False, fontsize=7, handlelength=1.2, columnspacing=0.8)
    save(fig, output, "jvs-control")


def sweep(archive, output):
    rows = {row["model"]: row["levels"] for row in read(archive / "core/g1_results.json")}
    panels = [
        ("reverb", "(a) Synthetic reverberation", "Wet fraction", (0.1, 0.2, 0.3, 0.5)),
        ("codec", "(b) EnCodec", "Bitrate (kb/s)", (1.5, 3, 6, 12, 24)),
        ("mp3", "(c) MP3", "Bitrate (kb/s)", (32, 64, 128)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.15, 2.65), sharey=True)
    fig.subplots_adjust(left=0.092, right=0.985, bottom=0.30, top=0.88, wspace=0.13)
    for ax, (key, title, label, settings) in zip(axes, panels):
        for model, name, color, style, marker in MODELS:
            values = [rows[model][f"{key}@{v:g}"]["effect_pts"] for v in settings]
            ax.plot(settings, values, label=name, color=color, linestyle=style,
                    marker=marker, markersize=3.6, linewidth=1.18, markerfacecolor="white")
        ax.set_title(title, loc="left", fontsize=8.6)
        ax.set(xlabel=label, ylim=(-7, 96), yticks=(0, 20, 40, 60, 80))
        if key != "reverb":
            ax.set_xscale("log", base=2)
            ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xticks(settings, [f"{v:g}" for v in settings])
        clean_axes(ax, "y")
        ax.axhline(0, color=MUTED, linewidth=0.65)
    axes[0].set_ylabel("Change from clean (percentage points)", fontsize=7.7)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=5, loc="lower center", frameon=False,
               bbox_to_anchor=(0.53, 0.015), fontsize=8, columnspacing=1.5)
    save(fig, output, "gtsinger-sweep")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Path to singer-or-studio-paper/archive")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "figures")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    factorial(args.archive, args.output)
    sweep(args.archive, args.output)


if __name__ == "__main__":
    main()
