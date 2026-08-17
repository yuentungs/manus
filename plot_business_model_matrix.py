"""Render market-priority ranks for three jewellery business-model assumptions."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "src" else SCRIPT_PATH.parent
SCORES = ROOT / "outputs" / "business_model_priority_scores.csv"
ASSUMPTIONS = ROOT / "outputs" / "business_model_assumptions.csv"
OUT = ROOT / "figures" / "business_model_priority_matrix.png"
if not SCORES.exists():
    SCORES = ROOT / "business_model_priority_scores.csv"
    ASSUMPTIONS = ROOT / "business_model_assumptions.csv"
    OUT = ROOT / "business_model_priority_matrix.png"

MODEL_ORDER = ["international_brand", "small_independent", "ecommerce_cross_border"]
DISPLAY_LABELS = ["International\nbrand", "Small /\nindependent", "E-commerce /\ncross-border"]


def main() -> None:
    scores = pd.read_csv(SCORES).sort_values("rank_international_brand")
    assumptions = pd.read_csv(ASSUMPTIONS).set_index("model")
    rank_columns = [f"rank_{model}" for model in MODEL_ORDER]
    matrix = scores[rank_columns].to_numpy()

    fig, ax = plt.subplots(figsize=(10.4, 6.1))
    heatmap = ax.imshow(matrix, cmap="YlGnBu_r", vmin=1, vmax=6, aspect="auto")

    ax.set_xticks(np.arange(len(DISPLAY_LABELS)), labels=DISPLAY_LABELS, fontweight="bold")
    ax.set_yticks(np.arange(len(scores)), labels=scores["country"])
    ax.set_title("APAC Jewellery Market Priorities — Business-Model Rank Matrix", fontweight="bold", pad=16)

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

    for position in [0.5, 1.5, 2.5, 3.5, 4.5]:
        ax.axhline(position, color="white", linewidth=1.4)

    weights = []
    for model in MODEL_ORDER:
        row = assumptions.loc[model]
        weights.append(
            f"{row['label']}: PP {row['purchasing_power']:.0%} | Digital {row['digital_readiness']:.0%} | Urban {row['urban_retail_context']:.0%} | Scale {row['economic_scale']:.0%}"
        )
    fig.text(0.01, 0.055, "\n".join(weights), fontsize=8.3)
    fig.text(
        0.01,
        0.01,
        "Finding: Singapore and Hong Kong are #1/#2 in all models; Indonesia rises only under the scale-weighted e-commerce assumption.",
        fontsize=8.5,
    )
    colourbar = fig.colorbar(heatmap, ax=ax, fraction=0.035, pad=0.03)
    colourbar.set_label("Rank (1 = highest stated-model signal)")
    fig.tight_layout(rect=(0, 0.15, 1, 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220, bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
