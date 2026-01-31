# Task 1: Disease & Target Landscape Analysis

## Disease Area
**Oncology**

## Selected Disease
**Glioblastoma (GBM)**

## 1. Disease Overview and Clinical Need


Glioblastoma multiforme (GBM) is an aggressive and lethal primary brain tumor of neuroectodermal origin that constitute for more than 50% of all glioma with high incidence rate in adults. it is characterized by rapid growth, extensive invasiveness, and profound molecular and cellular heterogeneity. Despite advances in neuro-oncology, GBM continues to pose significant therapeutic challenges and remian largely incurable.

The current standard therapy for GBM involves tumor mass removal using surgical resection, which is followed by radiotherapy and temozolomide-based chemotherapy treatments. However, a high rate of relapse, resistance developement of the cancer cells, and severe deterioration of the patients quality of life make such treatments ineffective. As a result, the median overall survival remains approximately 14-16 months, with a five year survical rate of less than 5%.
The lack of validated molecular targets and presence of blood-brain barrier severely restricts drug penetration into the central nervous system, limiting the effectiveness of many systemic therapies. Additionally, GBM tumors exhibit extensive intratumoral heterogeneity, allowing subclonak populations to evade targeted treatments and drive reccurence. Importantly, there is a lack of well-validated molecular targets that can be safely and effectively modulated in the brain. 

Major clinical and biological challenges associated with GBM are:

- High molecular and cellular hetrogeneity
- Rapid tumor progression and recurrence
- Resistance to chemotherapy and radiotherapy
- Limited success of targeted therapies
- Strong involvement of immune suppression and inflammatory signaling
- Restricted drug delivery due to the blood-brain barrier

These challenges highlight the significant clinical need for novel, biology-driven therapeutic strategies that target core oncogenic mechanism in GBM.

## 2. Target Identification Stratergy

## Objective
Potential drug targets were idnetified using publically available databases and curated resourses, as mentioned in the task description. This will help to capture multiple evidences, including genetic association, curated disease knowledge and pathway-level involvement.

**Open Target platform** -Used to assess disease-Gene association with supporting genetic, functional and clinical evidences 
**DisGeNET** - Curated disease-gene relationship derived from expert-reviewed sources and literature.
**GWAS catalog** - Genes associated with disease through genome-wide association studies, providing population-level genetic evidences.
**Pathway Datbase (KEGG/Reactome)** - Genes involvement in disease relevant signaling pathways and oncogenic mechanism.


Targets were identified from each of these souirces and integrated at the gene level to reduce source-specific bias.

## 3. Evidence integration and Target identification

Disease-Gene level evidences from Open Target, DisGeNET, GWAS catalog and KEGG pathway analysis were downloaded, cleaned and integrated into unified dataset. Each gene was assigned binary evidence flags based on its presence in respective data sources. 

An evidence count score calculated for each gene, representing the number of independent sources supporting GBM association. This will help to prioritize targets supported by multiple evidences.

Genes supported by three or more independent sources were defined as core candidate targets and selected for downstream analysis.

## 4. Candidate Targets

Based on evidence integration and filtering, the following biologically relevant targets were shortlisted.

| Target     | Key Biological Role and Relevance in GBM                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EGFR**   | Frequently amplified or mutated in GBM, driving aberrant growth factor signaling and tumor proliferation. EGFR is overexpressed in approximately 60% of primary glioblastomas compared to ~10% of secondary glioblastomas and is characteristic of highly aggressive tumor phenotypes. In addition to overexpression, constitutively active variants such as EGFRvIII further enhance oncogenic signaling and therapeutic resistance. |
| **PTEN**   | Tumor suppressor that negatively regulates the PI3K–AKT–mTOR signaling pathway. PTEN is frequently mutated, deleted, or epigenetically silenced in GBM, particularly in primary (de novo) tumors. Loss of PTEN leads to enhanced cell survival, angiogenesis, metabolic reprogramming, and resistance to therapy. Reduced PTEN expression is associated with poor clinical prognosis.                                                 |
| **TP53**   | Central regulator of DNA damage response, apoptosis, and genomic stability. The p53–ARF–MDM2 pathway is deregulated in approximately 84% of GBM cases. TP53 mutations occur in ~28–30% of primary GBM and rise to 65–90% in secondary GBM, where they frequently co-occur with IDH1 mutations, contributing to tumor evolution and therapy resistance.                                                                                |
| **CDKN2A** | Cell cycle regulator encoding p16<sup>INK4A</sup> and p14<sup>ARF</sup>, which inhibit CDK4/6-mediated G1–S phase transition. Homozygous deletion of CDKN2A occurs in ~60% of GBM cases and drives uncontrolled proliferation. Loss of CDKN2A is also linked to metabolic vulnerabilities, including increased sensitivity to ferroptosis, highlighting potential therapeutic opportunities.                                          |



These targets were selected based on support from multiple independent evidence sources, strong involvement in GBM relevant pathwyas, known functional relevance in tumor pregression and resistance, and representing both oncogenic drivers and tumor suppressor pathways. 


# Task 2: Target Prioritization

## Objective

After identifying a set of GBM-associated candidate genes, the next step is to prioritize these targets. The objective here is to rank genes to understand why these targets stand out based on different types of supporting evidence.

Simple scoring approach has been choosen to make prioritization east interpret and allows each decision to be linked to biological relevance.

Each target was evaluated using four evidencbased features:

**1. Genetic evidence/Scoring:** Genetic support derived from Open Target and the GWAS catalog was used. Targets supported by human genetic data were given higher importance.

**2. Disease Association (Disease Score):** Curated disease-gene association from DisGeNET were used to capture well-established links reported in expert-reviewed lioterature.

**Pathway Involvement (Pathway SCore):** Genes participating in GBM-relevant signaling pathways were identified using KEGG pathway data. This feature reflects involvement in known oncogenic processes.

**Druggability (Druggability Scre):** open Targets annotations were used as a proxy for therapeutic feasibility, indicating whether a gene has characteristics that make it more likely for pharmacological intervention.

All features were encoded in a binary manner, reflecting the presence or absence of supporting evidence.

## Scoring and Ranking Stratergy

A weighted linear scoring model was used to compute final priority score for each target. Genetic evidence was given the highest weight, followeed by pathway involvement and curated disease knowledge, while druggability was included as a supporting factor.This reflects genetically supported and pathway-relevant targets are more likely to be biologically important in GBM. Targets were ranked based on their composite scores to generate a prioritized list for further downstream analysis.

## Visualization and Interpretation

Target Prioritization Bar Plot: Shows the relative ranking of targets based on their final Priority Score helps to compare overall evidence support.

Feature Contribution Heatmap: Highlights how different evidence types contribute to each target’s score to understand similarities and differences between candidates.

Using this prioritization framework, a small set of highly supported targets including EGFR, PTEN, TP53, and CDKN2A emerged as top candidates. These genes were taken forward for pathway and network level validation in Task 4.

## Assumptions

- Public databases Open Targets, DisGeNET, GWAS Catalog, and KEGG provide reliable and curated disease–gene associations for glioblastoma.
- Genes supported by multiple independent data sources are more likely to play an important biological role in GBM.
- Binary evidence flags (presence or absence in a data source) are sufficient for an initial, high-level prioritization.
- Pathway(KEGG) reflects functional relevance to GBM-related biological processes.
- Genetic and curated disease evidence are weighted more heavily as they reflect stronger causal or biological support.

## Limitations

- The analysis relies on publicly available datasets, which may be incomplete or biased toward well-studied genes.
- GWAS evidence for GBM is limited, strict significance thresholds may exclude biologically relevant genes.
- Binary scoring does not capture the full strength or confidence of individual evidence sources.
- Druggability was approximated using available annotations and does not account for blood–brain barrier penetration or clinical feasibility.
- Protein interactions and pathway involvement were not experimentally validated and should be interpreted as hypothesis generating.
- The scoring framework is simple and designed for interpretability rather than predictive modeling.

# Task 4: Target Validation: Pathway & Network Analysis

## Objective

To validate the shortlisted glioblastoma targets by examining their interaction networks and pathways. Protein–protein interaction (PPI) and pathway analysis were used to understand the biological connectivity, functional importance, and potential safety considerations of the prioritized targets.

## Data Source and Approach

Protein–protein interaction data were obtained from the STRING database, which integrates experimental evidence, curated databases, co-expression patterns, and literature-based associations.

The analysis focused on:

- Core GBM targets identified from Task 1 and Task 2
- High-confidence interactions (STRING combined score)
- Interactions directly or indirectly linking GBM-relevant oncogenic pathways

The STRING interaction results were downloaded as a TSV file and processed using Python for filtering and interpretation.

## Network Construction and Filtering

- Nodes represent proteins (genes)
- Edges represent functional or physical protein–protein interactions
- Interactions with higher combined confidence scores (>=0.4) were prioritized
- The network was filtered to retain interactions involving at least one core GBM target

This approach preserves biologically meaningful connections relevant to glioblastoma biology.

## Key Interacting Partners and Network Insights

A protein–protein interaction network was built using STRING to understand how the prioritized GBM targets are connected at the pathway level. The final network contained 14 proteins (nodes) connected by 46 interactions (edges), showing that these proteins are closely linked rather than acting independently.

**Key Interacting Partners**

Among the proteins in the network, TP53, CDKN2A, EGFR, and PTEN showed the highest number of interactions, indicating that they act as central regulators. Other interacting partners such as MGMT and MDM4 were also present, supporting the involvement of DNA repair and p53-related signaling in glioblastoma.

**Mechanism of Action and Safety Considerations**

The network highlights key biological processes such as cell-cycle regulation, growth factor signaling, DNA damage response, and apoptosis. Highly connected proteins like TP53 and EGFR play essential roles in both tumor and normal cellular functions. While this makes them biologically important targets, direct inhibition may also disrupt normal pathways and increase the risk of side effects.To address this, alternative strategies such as targeting downstream signaling components, pathway regulators, or using combination approaches may offer improved tumor specificity while reducing off-target effects.

**Network Centrality and Redundancy**

The high number of interactions within a small network suggests strong centrality of the core targets and limited pathway redundancy. This means that changes to these proteins are likely to have broad effects on tumor behavior, but compensatory signaling through related pathways may still occur.

## References

1. https://journals.lww.com/cancerjournal/fulltext/2022/18030/an_overview_of_targets_and_therapies_for.1.aspx  
2. https://www.sciencedirect.com/science/article/pii/S0031699724012614  
3. https://pmc.ncbi.nlm.nih.gov/articles/PMC4101015/  
4. https://www.cell.com/cancer-cell/fulltext/S1535-6108(23)00168-X  
5. https://pmc.ncbi.nlm.nih.gov/articles/PMC6162501/  
6. https://www.sciencedirect.com/science/article/pii/S0753332222015931  
7. https://pmc.ncbi.nlm.nih.gov/articles/PMC5210543/  
8. https://www.biorxiv.org/content/10.1101/2025.03.06.641926v2.full  
