"""
Task 2: Target Prioritization Using Evidence-Based Scoring

This script ranks core GBM targets using a simple,
interpretable scoring framework based on genetic evidence,
disease association, pathway involvement, and druggability.
Visualization using barplot and heatplot.
"""

import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# File paths
INPUT_FILE = "D:/Progenica_task-GBM _target_discovery/results/GBM_core_targets.csv"
OUTPUT_TABLE = "D:/Progenica_task-GBM _target_discovery/results/GBM_task2_target_ranking.csv"

BARPLOT_FILE = "D:/Progenica_task-GBM _target_discovery/figures/GBM_Task2_Barplot.png"
HEATMAP_FILE = "D:/Progenica_task-GBM _target_discovery/figures/GBM_Task2_Heatmap.png"

# Load core targets
df = pd.read_csv(INPUT_FILE)

# Feature definition

# Genetic evidence
df["GeneticScore"] = df["OpenTargets"] + df["GWAS"]

# Curated disease knowledge
df["DiseaseScore"] = df["DisGeNET"]

# Pathway involvement
df["PathwayScore"] = df["KEGG"]

# Druggability
df["DruggabilityScore"] = df["OpenTargets"]

# Composite priority score

df["PriorityScore"] = (
    3.0 * df["GeneticScore"] +
    2.0 * df["PathwayScore"] +
    1.5 * df["DiseaseScore"] +
    1.0 * df["DruggabilityScore"]
)

df = df.sort_values("PriorityScore", ascending=False)

# Save ranked table
df.to_csv(OUTPUT_TABLE, index=False)
print("Target ranking saved:", OUTPUT_TABLE)

# Bar plot

df_plot = df.sort_values("PriorityScore", ascending=True)

width, height = 900, 420
left_margin = 220
right_margin = 80
top_margin = 70
bar_height = 34
bar_gap = 18

img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

try:
    title_font = ImageFont.truetype("arial.ttf", 20)
    label_font = ImageFont.truetype("arial.ttf", 14)
    value_font = ImageFont.truetype("arial.ttf", 13)
except:
    title_font = label_font = value_font = ImageFont.load_default()

max_score = df_plot["PriorityScore"].max()
plot_width = width - left_margin - right_margin

# Title
draw.text(
    (width // 2 - 280, 20),
    "Evidence-Based Prioritization of Glioblastoma Targets",
    fill="black",
    font=title_font
)

# Bars
for i, row in enumerate(df_plot.itertuples()):
    y = top_margin + i * (bar_height + bar_gap)
    bar_len = int((row.PriorityScore / max_score) * plot_width)

    # Gene label
    draw.text(
        (20, y + 7),
        row.gene,
        fill="black",
        font=label_font
    )

    # Bar
    draw.rectangle(
        [left_margin, y, left_margin + bar_len, y + bar_height],
        fill=(70, 130, 180)  # steel blue
    )

    # Score label
    draw.text(
        (left_margin + bar_len + 8, y + 7),
        f"{row.PriorityScore:.1f}",
        fill="black",
        font=value_font
    )

img.save(BARPLOT_FILE)

#  Heatmap

features = [
    "GeneticScore",
    "DiseaseScore",
    "PathwayScore",
    "DruggabilityScore"
]

data = df[features].values.astype(float)
norm_data = data / data.max()

cell_w = 120
cell_h = 45
left_margin = 190
top_margin = 70

img_w = left_margin + cell_w * len(features) + 30
img_h = top_margin + cell_h * len(df) + 30

img = Image.new("RGB", (img_w, img_h), "white")
draw = ImageDraw.Draw(img)

try:
    header_font = ImageFont.truetype("arial.ttf", 14)
    cell_font = ImageFont.truetype("arial.ttf", 12)
except:
    header_font = cell_font = ImageFont.load_default()

# Title
draw.text(
    (img_w // 2 - 210, 20),
    "Feature Contribution Heatmap for Prioritized GBM Targets",
    fill="black",
    font=header_font
)

# Column headers
for j, feat in enumerate(features):
    draw.text(
        (left_margin + j * cell_w + 10, top_margin - 35),
        feat,
        fill="black",
        font=header_font
    )

# Row labels
for i, gene in enumerate(df["gene"]):
    draw.text(
        (20, top_margin + i * cell_h + 12),
        gene,
        fill="black",
        font=header_font
    )

# Heatmap cells
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        val = norm_data[i, j]
        blue_intensity = int(255 * val)
        color = (230 - blue_intensity, 230 - blue_intensity, 255)

        x0 = left_margin + j * cell_w
        y0 = top_margin + i * cell_h
        x1 = x0 + cell_w
        y1 = y0 + cell_h

        draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")
        draw.text(
            (x0 + 50, y0 + 12),
            str(int(data[i, j])),
            fill="black",
            font=cell_font
        )

img.save(HEATMAP_FILE)
