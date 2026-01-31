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
    "D:/Prognica_task-GBM _target_discovery/Target_data/open_target_gbm.tsv",
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
    "D:/Prognica_task-GBM _target_discovery/clean_data/opentargets_clean.csv",
    index=False
)

print("Open Targets cleaned:", ot_clean.shape)


# ============================================================
# 2. DISGENET – curated disease–gene knowledge
# ============================================================

dg = pd.read_csv(
    "D:/Prognica_task-GBM _target_discovery/Target_data/disgenet_gbm.tsv",
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
    "D:/Prognica_task-GBM _target_discovery/clean_data/disgenet_clean.csv",
    index=False
)

print("DisGeNET cleaned:", dg_clean.shape)


# ============================================================
# 3. GWAS CATALOG – genetic association evidence
# ============================================================

gwas = pd.read_csv(
    "D:/Prognica_task-GBM _target_discovery/Target_data/gwas_catalog_gbm.tsv",
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
    "D:/Prognica_task-GBM _target_discovery/clean_data/gwas_clean.csv",
    index=False
)

print("GWAS cleaned:", gwas_clean.shape)


# ============================================================
# 4. KEGG – pathway-driven gene extraction (KGML)
# ============================================================

# KEGG KGML-Gene Symbol Extractor


KGML_FILE = "D:/Prognica_task-GBM _target_discovery/Target_data/hsa05214.xml"
OUTPUT_FILE = "D:/Prognica_task-GBM _target_discovery/clean_data/kegg_genes.csv"

# Parse KGML
tree = ET.parse(KGML_FILE)
root = tree.getroot()

kegg_entrez_ids = []

for entry in root.findall("entry"):
    if entry.attrib.get("type") == "gene":
        name_field = entry.attrib.get("name")
        if name_field:
            for gid in name_field.split():
                if gid.startswith("hsa:"):
                    kegg_entrez_ids.append(gid.replace("hsa:", ""))

kegg_entrez_ids = sorted(set(kegg_entrez_ids))

print(f"[INFO] Number of KEGG Entrez IDs extracted: {len(kegg_entrez_ids)}")
print(f"[INFO] Example Entrez IDs: {kegg_entrez_ids[:10]}")

# Entrez ID → Gene Symbol Mapping
print("[INFO] Downloading KEGG human gene mapping...")

kegg_text = requests.get("https://rest.kegg.jp/list/hsa").text.strip().split("\n")

entrez_to_symbol = {}

for line in kegg_text:
    if not line:
        continue
    left, right = line.split("\t", 1)
    entrez = left.replace("hsa:", "").strip()
    symbol = right.split(";")[0].strip()   # OFFICIAL gene symbol
    entrez_to_symbol[entrez] = symbol

# Map Entrez IDs
mapped_symbols = [
    entrez_to_symbol[e] for e in kegg_entrez_ids if e in entrez_to_symbol
]

mapped_symbols = sorted(set(mapped_symbols))

print(f"[INFO] Number of gene symbols mapped: {len(mapped_symbols)}")
print(f"[INFO] Example gene symbols: {mapped_symbols[:10]}")

# Save Clean Gene List
kegg_df = pd.DataFrame({"gene": mapped_symbols})
kegg_df.to_csv(OUTPUT_FILE, index=False)

print(f"[SUCCESS] KEGG gene list saved to:\n{OUTPUT_FILE}")

# File paths
INPUT_FILE = "D:/Prognica_task-GBM _target_discovery/clean_data/kegg_genes.csv"
OUTPUT_FILE = "D:/Prognica_task-GBM _target_discovery/clean_data/kegg_genes_clean.csv"

# Load file
df = pd.read_csv(INPUT_FILE)

# Check data
print("Raw rows:", df.shape[0])
print(df.head(3))

def extract_gene_symbol(text):
    """
    Extract official gene symbol from KEGG CDS-style annotation
    """
    if pd.isna(text):
        return None
    
    text = str(text)
    
    # Split by TAB delimiter
    parts = text.split("\t")
    if len(parts) < 3:
        return None
    
    # Last field with gene names
    gene_part = parts[-1]
    
    # First name before comma is official symbol
    symbol = gene_part.split(",")[0].strip()
    
    return symbol

# Apply extraction
df["gene_clean"] = df["gene"].apply(extract_gene_symbol)

# Keep clean gene list
kegg_clean = (
    df[["gene_clean"]]
    .dropna()
    .drop_duplicates()
    .rename(columns={"gene_clean": "gene"})
)

print("Clean gene count:", kegg_clean.shape[0])
print("Example genes:", kegg_clean["gene"].head(10).tolist())

# Save
kegg_clean.to_csv(OUTPUT_FILE, index=False)

print(f"[SUCCESS] Clean KEGG gene list saved to:\n{OUTPUT_FILE}")


# ============================================================
# 5. INTEGRATION – evidence consolidation across sources
# ============================================================

ot = pd.read_csv("D:/Prognica_task-GBM _target_discovery/clean_data/opentargets_clean.csv")
dg = pd.read_csv("D:/Prognica_task-GBM _target_discovery/clean_data/disgenet_clean.csv")
gwas = pd.read_csv("D:/Prognica_task-GBM _target_discovery/clean_data/gwas_clean.csv")
kegg = pd.read_csv("D:/Prognica_task-GBM _target_discovery/clean_data/kegg_genes_clean.csv")

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
    "D:/Prognica_task-GBM _target_discovery/results/GBM_all_targets_evidence.csv",
    index=False
)

# Core targets: ≥3 independent evidence sources
core_targets = master[master["EvidenceCount"] >= 3]

core_targets.sort_values("EvidenceCount", ascending=False).to_csv(
    "D:/Prognica_task-GBM _target_discovery/results/GBM_core_targets.csv",
    index=False
)

print("Total targets:", master.shape[0])
print("Core targets (≥3 sources):", core_targets.shape[0])
print(core_targets.head(10))