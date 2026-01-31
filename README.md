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

Potential drug targets were idnetified using publically available databases and curated resourses, as mentioned in the task description. This will help to capture multiple evidences, including genetic association, curated disease knowledge and pathway-level involvement.

**Open Target platform** -Used to assess disease-Gene association with supporting genetic, functional and clinical evidences 
**DisGeNET** - Curated disease-gene relationship derived from expert-reviewed sources and literature.
**GWAS catalog** - Genes associated with disease through genome-wide association studies, providing population-level genetic evidences.
**Pathway Datbase (KEGG/Reactome)** - Genes involvement in disease relevant signaling pathways and oncogenic mechanism.


Targets were identified from each of these souirces and integrated at the gene level to reduce source-specific bias.

# 3. Evidence integration and Target identification

Disease-Gene level evidences from Open Target, DisGeNET, GWAS catalog and KEGG pathway analysis were downloaded, cleaned and integrated into unified dataset. Each gene was assigned binary evidence flags based on its presence in respective data sources. 

An evidence count score calculated for each gene, representing the number of independent sources supporting GBM association. This will help to prioritize targets supported by multiple evidences.

Genes supported by three or more independent sources were defined as core candidate targets and selected for downstream analysis.

# 4. Candidate Targets

Based on evidence integration and filtering, the following biologically relevant targets were shortlisted.

| Target     | Key Biological Role and Relevance in GBM                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EGFR**   | Frequently amplified or mutated in GBM, driving aberrant growth factor signaling and tumor proliferation. EGFR is overexpressed in approximately 60% of primary glioblastomas compared to ~10% of secondary glioblastomas and is characteristic of highly aggressive tumor phenotypes. In addition to overexpression, constitutively active variants such as EGFRvIII further enhance oncogenic signaling and therapeutic resistance. |
| **PTEN**   | Tumor suppressor that negatively regulates the PI3K–AKT–mTOR signaling pathway. PTEN is frequently mutated, deleted, or epigenetically silenced in GBM, particularly in primary (de novo) tumors. Loss of PTEN leads to enhanced cell survival, angiogenesis, metabolic reprogramming, and resistance to therapy. Reduced PTEN expression is associated with poor clinical prognosis.                                                 |
| **TP53**   | Central regulator of DNA damage response, apoptosis, and genomic stability. The p53–ARF–MDM2 pathway is deregulated in approximately 84% of GBM cases. TP53 mutations occur in ~28–30% of primary GBM and rise to 65–90% in secondary GBM, where they frequently co-occur with IDH1 mutations, contributing to tumor evolution and therapy resistance.                                                                                |
| **CDKN2A** | Cell cycle regulator encoding p16<sup>INK4A</sup> and p14<sup>ARF</sup>, which inhibit CDK4/6-mediated G1–S phase transition. Homozygous deletion of CDKN2A occurs in ~60% of GBM cases and drives uncontrolled proliferation. Loss of CDKN2A is also linked to metabolic vulnerabilities, including increased sensitivity to ferroptosis, highlighting potential therapeutic opportunities.                                          |



These targets were selected based on support from multiple independent evidence sources, strong involvement in GBM relevant pathwyas, known functional relevance in tumor pregression and resistance, and representing both oncogenic drivers and tumor suppressor pathways. 

## Reference

https://journals.lww.com/cancerjournal/fulltext/2022/18030/an_overview_of_targets_and_therapies_for.1.aspx
https://www.biorxiv.org/content/10.1101/2025.03.06.641926v2.full
https://www.sciencedirect.com/science/article/pii/S0031699724012614
https://pmc.ncbi.nlm.nih.gov/articles/PMC4101015/
https://www.cell.com/cancer-cell/fulltext/S1535-6108(23)00168-X
https://pmc.ncbi.nlm.nih.gov/articles/PMC6162501/#:~:text=TP53%20is%20one%20of%20the,apoptosis%2C%20and%20cancer%20cell%20stemness.
https://pmc.ncbi.nlm.nih.gov/articles/PMC6162501/#:~:text=TP53%20is%20one%20of%20the,apoptosis%2C%20and%20cancer%20cell%20stemness.
https://www.sciencedirect.com/science/article/pii/S0753332222015931#:~:text=Abstract,regulated%20by%20non%2Dcoding%20RNAs.
