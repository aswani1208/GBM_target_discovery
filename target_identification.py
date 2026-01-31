"""
GBM Target Identification Pipeline

This script integrates multiple public resources (Open Targets, DisGeNET,
GWAS Catalog, and KEGG) to identify and prioritize biologically supported
targets for Glioblastoma.

Steps:
1. Clean and harmonize gene-level evidence from each source
2. Extract KEGG pathway genes from KGML
3. Integrate all evidence at the gene level
4. Identify core targets supported by ≥3 independent sources
"""

import pandas as pd
import xml.etree.ElementTree as ET
import requests

# ============================================================
# 1. OPEN TARGETS – disease–gene association strength
# ============================================================

ot = pd.read_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/open_target_gbm.tsv",
    sep="\t"
)

# Standardize gene symbols
ot["gene"] = ot["symbol"].astype(str).str.upper().str.strip()

# Keep relevant columns only
ot_clean = ot[["gene", "globalScore"]].copy()

# Remove empty gene symbols
ot_clean = ot_clean[ot_clean["gene"] != ""]

# Filter weak disease associations
ot_clean = ot_clean[ot_clean["globalScore"] >= 0.2]

# Deduplicate by keeping strongest association per gene
ot_clean = (
    ot_clean
    .sort_values("globalScore", ascending=False)
    .drop_duplicates("gene")
)

ot_clean.to_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/opentargets_clean.csv",
    index=False
)

print("Open Targets cleaned:", ot_clean.shape)


# ============================================================
# 2. DISGENET – curated disease–gene knowledge
# ============================================================

dg = pd.read_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/disgenet_gbm.tsv",
    sep="\t"
)

dg["gene"] = dg["gene_symbol"].astype(str).str.upper().str.strip()

# Keep score if available
if "score" in dg.columns:
    dg_clean = dg[["gene", "score"]].copy()
else:
    dg_clean = dg[["gene"]].copy()
    dg_clean["score"] = 1  # fallback for presence-only data

dg_clean = dg_clean[dg_clean["gene"] != ""]

dg_clean = (
    dg_clean
    .sort_values("score", ascending=False)
    .drop_duplicates("gene")
)

dg_clean.to_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/disgenet_clean.csv",
    index=False
)

print("DisGeNET cleaned:", dg_clean.shape)


# ============================================================
# 3. GWAS CATALOG – genetic association evidence
# ============================================================

gwas = pd.read_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/gwas_catalog_gbm.tsv",
    sep="\t"
)

gwas = gwas[["MAPPED_GENE", "P-VALUE"]].dropna(subset=["MAPPED_GENE"])

# Split multi-gene annotations
gwas["gene"] = (
    gwas["MAPPED_GENE"]
    .astype(str)
    .str.split(",")
)

gwas = gwas.explode("gene")
gwas["gene"] = gwas["gene"].str.upper().str.strip()

# Genome-wide significance threshold
gwas_sig = gwas[gwas["P-VALUE"] < 5e-8]

# If no significant hits, retain unique mapped genes
if gwas_sig.empty:
    gwas_clean = gwas[["gene"]].drop_duplicates()
else:
    gwas_clean = gwas_sig[["gene"]].drop_duplicates()

gwas_clean.to_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/gwas_clean.csv",
    index=False
)

print("GWAS cleaned:", gwas_clean.shape)


# ============================================================
# 4. KEGG – pathway-driven gene extraction (KGML)
# ============================================================

KGML_FILE = "D:/Progenica_task-GBM _target_discovery/Target_data/hsa05214.xml"

tree = ET.parse(KGML_FILE)
root = tree.getroot()

entrez_ids = []

for entry in root.findall("entry"):
    if entry.attrib.get("type") == "gene":
        names = entry.attrib.get("name", "")
        for gid in names.split():
            if gid.startswith("hsa:"):
                entrez_ids.append(gid.replace("hsa:", ""))

entrez_ids = sorted(set(entrez_ids))

# Map Entrez → gene symbol using KEGG REST
kegg_map = requests.get(
    "https://rest.kegg.jp/list/hsa"
).text.strip().split("\n")

entrez_to_gene = {}
for line in kegg_map:
    eid, desc = line.split("\t", 1)
    entrez_to_gene[eid.replace("hsa:", "")] = desc.split(";")[0].strip()

kegg_genes = sorted({
    entrez_to_gene[e]
    for e in entrez_ids
    if e in entrez_to_gene
})

kegg_clean = pd.DataFrame({"gene": kegg_genes})

kegg_clean.to_csv(
    "D:/Progenica_task-GBM _target_discovery/Target_data/kegg_genes_clean.csv",
    index=False
)

print("KEGG genes extracted:", kegg_clean.shape)


# ============================================================
# 5. INTEGRATION – evidence consolidation across sources
# ============================================================

ot = pd.read_csv("D:/Progenica_task-GBM _target_discovery/Target_data/opentargets_clean.csv")
dg = pd.read_csv("D:/Progenica_task-GBM _target_discovery/Target_data/disgenet_clean.csv")
gwas = pd.read_csv("D:/Progenica_task-GBM _target_discovery/Target_data/gwas_clean.csv")
kegg = pd.read_csv("D:/Progenica_task-GBM _target_discovery/Target_data/kegg_genes_clean.csv")

# Evidence flags
ot_f = ot[["gene"]].drop_duplicates().assign(OpenTargets=1)
dg_f = dg[["gene"]].drop_duplicates().assign(DisGeNET=1)
gwas_f = gwas[["gene"]].drop_duplicates().assign(GWAS=1)
kegg_f = kegg[["gene"]].drop_duplicates().assign(KEGG=1)

# Merge all sources
master = (
    ot_f
    .merge(dg_f, on="gene", how="outer")
    .merge(kegg_f, on="gene", how="outer")
    .merge(gwas_f, on="gene", how="outer")
)

master.fillna(0, inplace=True)

# Evidence count per gene
master["EvidenceCount"] = (
    master["OpenTargets"] +
    master["DisGeNET"] +
    master["KEGG"] +
    master["GWAS"]
)

# Save all targets
master.sort_values("EvidenceCount", ascending=False).to_csv(
    "D:/Progenica_task-GBM _target_discovery/results/GBM_all_targets_evidence.csv",
    index=False
)

# Core targets: ≥3 independent evidence sources
core_targets = master[master["EvidenceCount"] >= 3]

core_targets.sort_values("EvidenceCount", ascending=False).to_csv(
    "D:/Progenica_task-GBM _target_discovery/results/GBM_core_targets.csv",
    index=False
)

print("Total targets:", master.shape[0])
print("Core targets (≥3 sources):", core_targets.shape[0])
print(core_targets.head(10))