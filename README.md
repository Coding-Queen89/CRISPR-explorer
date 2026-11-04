# CRISPR gRNA Designer

## Objective

Build a learning prototype that makes the first steps of CRISPR guide
RNA selection transparent and reproducible.

The prototype focuses on:
- retrieving a DNA sequence from a public source (Ensembl REST),
- scanning both strands for SpCas9 PAM sites,
- applying a small set of explicit, rule-based sequence checks,
- and showing *why* each candidate passes or fails those checks.

The goal is not to predict experimental efficiency, but to demonstrate
how a transparent rule-based pipeline can support early-stage candidate
review for users who are new to the field.

## Problem

While existing tools and platforms like Benchling and CHOPCHOP already exist,
they often lack transparency in score generation and require a steep learning curve
from undergraduates or researchers and/or developers not mastering in the field.

## Target Users

- Students learning about CRISPR guide design.
- Developers interested in bioinformatics workflows.
- Researchers exploring an early-stage candidate search prototype.

## Core Workflow

Phase 0:
00. Analyze existing tools and limitations

Phase 1: gRNA Design — Backend
01. Input: Gene name (e.g., HBA1) ✔️
02. Ensembl REST API → Retrieve DNA sequence ✔️
03. PAM scanning (NGG) on both strands ✔️
04. Extract 20-nt candidates ✔️
05. Calculate GC content and poly-T flags ✔️
06. Output: List of candidates with rules (pass/fail) ✔️

Phase 2: Sequence Comparator
07. Input: Two FASTA sequences (wild-type vs. edited)
08. Biopython PairwiseAligner
09. Output: Mismatches, gaps, editing efficiency estimate

Phase 3: ClinVar Annotation
10. Input: Gene name or HGVS variant
11. NCBI E-utilities API → Search ClinVar
12. Output: Pathogenic variants and associated diseases

Phase 4: Frontend
13. Build React Frontend
14. Connect FastAPI routes
15. Test endpoints
16. Deploy MVP draft


## Initial Resources
- Ensembl API and website
- NCBI studies
- CRISPR GPT
- VEP and ClinVAR

## MVP

The first version will:

- take Gene Name as an Input and calling the Ensembl API
- finding suitable gRNAs with their respective GC
- Basic Visualization
- Compare two FASTA sequences
-

## Out of Scope

- No .ab1/.scf processing
- Genome-wide off-target search
- Prediction of experimental guide efficiency or knockout success
- Machine learning models of any kind
- Support for Cas enzymes other than SpCas9 (NGG PAM only)
- Multiple species or non-human genomes
- Primer design, HDR templates, or repair outcome prediction
- User accounts, authentication, or persistent user data
- Clinical or diagnostic use
- Benchmarks against wet-lab datasets

## Future Work

- Gene editing tool
- Disease correlation context for mutated genes (via ClinVar/VEP)
- Advanced visualisation
- Identifying and cancelling gRNA candidates in intron
