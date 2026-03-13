import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import glob
import os

# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
FILE_PATTERN = "pigments_*.csv"   # One CSV per year, or set SINGLE_FILE below
SINGLE_FILE  = None               # e.g. "all_pigments.csv" if one combined file

DATE_COL  = "DateTime"
LAT_COL   = "Latitude"
LON_COL   = "Longitude"

# UK bounding box
LON_MIN, LON_MAX = -8, -2
LAT_MIN, LAT_MAX = 48, 54

PIGMENT_COLS = [
    "TChlA_ug/L", "TChl_ug/L", "AP_ug/L", "Degrad_products_ug/L",
    "TP_ug/L", "Fuc_ug/L", "Per_ug/L", "Hex_ug/L",
    "But_ug/L", "Allo_ug/L", "Chlb_ug/L", "Zea_ug/L",
]

PIGMENT_LABELS = {
    "TChlA_ug/L":           "Total Chlorophyll-a",
    "TChl_ug/L":            "Total Chlorophyll",
    "AP_ug/L":              "Alloxanthin + Peridinin",
    "Degrad_products_ug/L": "Degradation Products",
    "TP_ug/L":              "Total Pigments",
    "Fuc_ug/L":             "Fucoxanthin",
    "Per_ug/L":             "Peridinin",
    "Hex_ug/L":             "19'-Hexanoyloxyfucoxanthin",
    "But_ug/L":             "19'-Butanoyloxyfucoxanthin",
    "Allo_ug/L":            "Alloxanthin",
    "Chlb_ug/L":            "Chlorophyll-b",
    "Zea_ug/L":             "Zeaxanthin",
}

YEARS = [2020, 2021, 2022, 2023]
CMAP  = "viridis"

# ── 2. LOAD DATA ───────────────────────────────────────────────────────────────
def load_data():
    if SINGLE_FILE:
        df = pd.read_csv(SINGLE_FILE)
    else:
        files = sorted(glob.glob(FILE_PATTERN))
        if not files:
            raise FileNotFoundError(f"No files found matching: {FILE_PATTERN}")
        frames = []
        for f in files:
            tmp = pd.read_csv(f)
            if DATE_COL not in tmp.columns:
                year = int("".join(filter(str.isdigit, os.path.basename(f))))
                tmp["year"] = year
            frames.append(tmp)
        df = pd.concat(frames, ignore_index=True)

    # Parse DateTime
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], dayfirst=True, errors="coerce")
    df["year"]   = df[DATE_COL].dt.year

    # Filter to years of interest
    df = df[df["year"].isin(YEARS)]

    # Convert pigment columns to numeric
    for col in PIGMENT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing coordinates
    df = df.dropna(subset=[LAT_COL, LON_COL])

    return df

# ── 3. PLOT — one figure per pigment, 4 subplots (one per year) ────────────────
def plot_pigment_maps(df):
    for pigment in PIGMENT_COLS:
        if pigment not in df.columns:
            print(f"Skipping '{pigment}' — column not found.")
            continue

        label     = PIGMENT_LABELS.get(pigment, pigment)
        # Increased figure height to give room for the suptitle
        fig, axes = plt.subplots(1, 4, figsize=(20, 7))

        # suptitle with extra top padding
        fig.suptitle(f"{label} (μg/L) — Spatial Distribution by Year",
                     fontsize=15, fontweight="bold", y=0.98)

        # Shared colour scale across all years for this pigment
        all_vals   = df[pigment].dropna()
        vmin, vmax = np.percentile(all_vals, 2), np.percentile(all_vals, 98)

        for ax, year in zip(axes, YEARS):
            subset = df[df["year"] == year].dropna(subset=[pigment])

            ax.scatter(
                subset[LON_COL], subset[LAT_COL],
                c=subset[pigment], cmap=CMAP,
                vmin=vmin, vmax=vmax,
                s=30, alpha=0.8, edgecolors="none"
            )

            ax.set_xlim(LON_MIN, LON_MAX)
            ax.set_ylim(LAT_MIN, LAT_MAX)
            ax.set_title(str(year), fontsize=12, fontweight="bold", pad=8)
            ax.set_xlabel("Longitude", fontsize=9)
            ax.set_ylabel("Latitude", fontsize=9)
            ax.tick_params(labelsize=8)
            ax.set_facecolor("#d0e8f5")
            ax.grid(True, linestyle="--", alpha=0.3)
            ax.set_aspect("equal")

            # Sample count label
            ax.text(0.02, 0.98, f"n={len(subset)}",
                    transform=ax.transAxes, fontsize=8,
                    verticalalignment="top", color="black",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))

        # Shared colorbar
        cbar = fig.colorbar(
            cm.ScalarMappable(norm=mcolors.Normalize(vmin=vmin, vmax=vmax), cmap=CMAP),
            ax=axes, orientation="vertical", fraction=0.02, pad=0.04
        )
        cbar.set_label("Concentration (μg/L)", fontsize=10)

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)  # Reserve space for suptitle

        safe_name = pigment.replace("/", "_").replace(" ", "_")
        out_name  = f"map_{safe_name}.png"
        plt.savefig(out_name, dpi=150, bbox_inches="tight", pad_inches=0.5)
        print(f"Saved: {out_name}")
        plt.show()

# ── 4. MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    print(f"Loaded {len(df):,} rows | Years: {sorted(df['year'].unique())}")
    plot_pigment_maps(df)