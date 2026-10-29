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

01. Analyze existing tools and limitations
02. Select genomic data source (Ensembl REST)
03. Gene search module (Gene Name → DNA Sequence)
04. gRNA candidate generation (NGG scan, both strands)
05. Basic scoring (GC content, poly-T flag, PAM check)
06. Explainability module (per-candidate rule breakdown)
07. REST API (FastAPI)
08. React frontend (input + results table)
09. Visualizations (candidate table, filter status)
10. Integration frontend ↔ backend
11. Test with 2–3 example genes (BRCA1, TP53, etc.)
12. Deploy to server
13. Bug fixing and usability improvements


## Initial Resources
- Ensembl API and website
- NCBI studies
- CRISPR GPT
- VEP and ClinVAR

## MVP

The first version will:

- taking FASTA sequence as an Input and calling the Ensembl API
- finding suitable gRNAs with their respective GC
- Basic Visualization

## Out of Scope

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
