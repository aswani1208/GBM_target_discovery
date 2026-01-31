import pandas as pd

df = pd.read_csv(
    "D:/Prognica_task-GBM _target_discovery/network/string_interactions.tsv",
    sep="\t"
)

# Rename for convenience
df = df.rename(columns={"#node1": "geneA", "node2": "geneB"})

df[["geneA", "geneB", "combined_score"]].head()

core_targets = {"EGFR", "TP53", "PTEN", "CDKN2A"}

ppi_core = df[
    (df["geneA"].isin(core_targets)) |
    (df["geneB"].isin(core_targets))
]

# Optional confidence threshold (STRING default = 0.4)
ppi_core = ppi_core[ppi_core["combined_score"] >= 0.4]

print("Core-related interactions:", ppi_core.shape[0])
ppi_core.head()

import collections

# Count how often each gene appears
partners = (
    pd.concat([ppi_core["geneA"], ppi_core["geneB"]])
    .value_counts()
    .reset_index()
)

partners.columns = ["gene", "interaction_count"]

partners.head(10)

import pandas as pd

# ppi_core already filtered
degree_counts = (
    pd.concat([ppi_core["geneA"], ppi_core["geneB"]])
    .value_counts()
    .reset_index()
)

degree_counts.columns = ["gene", "interaction_count"]

print(degree_counts.head(10))
