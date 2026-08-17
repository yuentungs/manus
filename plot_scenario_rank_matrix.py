"""Render a decision-focused scenario-rank matrix for the APAC market study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "src" else SCRIPT_PATH.parent
SCORES = ROOT / "outputs" / "market_priority_scores.csv"
OUT = ROOT / "figures" / "scenario_rank_matrix.png"
if not SCORES.exists():
    SCORES = ROOT / "market_priority_scores.csv"
    OUT = ROOT / "scenario_rank_matrix.png"


def main() -> None:
    data = pd.read_csv(SCORES).sort_values("rank_balanced")
    rank_columns = ["rank_balanced", "rank_digital_first", "rank_scale_led"]
    labels = ["Balanced", "Digital-first", "Scale-led"]
    matrix = data[rank_columns].to_numpy()

    fig, ax = plt.subplots(figsize=(9.8, 5.7))
    heatmap = ax.imshow(matrix, cmap="YlGnBu_r", vmin=1, vmax=6, aspect="auto")

    ax.set_xticks(np.arange(len(labels)), labels=labels, fontweight="bold")
    ax.set_yticks(np.arange(len(data)), labels=data["country"])
    ax.set_title("APAC Jewellery Market Research Priorities — Scenario Rank Matrix", fontweight="bold", pad=14)

    for row_index in range(matrix.shape[0]):
        for col_index in range(matrix.shape[1]):
            rank = int(matrix[row_index, col_index])
            ax.text(
                col_index,
                row_index,
                f"#{rank}",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
                color="#132238" if rank == 3 else "white",
            )

    divider_positions = [0.5, 2.5, 3.5, 4.5]
    for position in divider_positions:
        ax.axhline(position, color="white", linewidth=1.5)

    wave_labels = {
        "Singapore": "Wave 1: Reference pilot",
        "Hong Kong SAR, China": "Wave 2: Premium/digital validation",
        "Malaysia": "Wave 2: Premium/digital validation",
        "Thailand": "Targeted opportunity scan",
        "Indonesia": "Wave 3: Scale-led hypothesis",
        "Vietnam": "Watchlist / evidence gathering",
    }
    for idx, market in enumerate(data["country"]):
        ax.text(
            3.02,
            idx,
            wave_labels[market],
            va="center",
            fontsize=9,
            color="#243447",
        )
    ax.set_xlim(-0.5, 4.65)

    colourbar = fig.colorbar(heatmap, ax=ax, fraction=0.035, pad=0.03)
    colourbar.set_label("Rank (1 = highest stated-scenario signal)")
    fig.text(
        0.01,
        0.01,
        "Finding: Singapore is the only stable #1; Indonesia's #6 digital-first / #2 scale-led spread requires conditional validation.",
        fontsize=8.5,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220, bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
