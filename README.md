# Interpretable Similarity Measures for Ontology Matching

University project (course *Pervasive Systems Architecture*, Research Master's in Intelligent Pervasive Systems, ISSAT Sousse) — **work in progress**.

The project compares several **interpretable similarity measures** (lexical, structural, embedding-based) for matching entities across ontologies, and tests whether **contextual information** (hierarchy, properties), extracted with SPARQL, improves the matching.

## Research questions

1. Which kind of similarity measure retrieves the correct correspondences best: lexical, structural or semantic (embeddings)?
2. Does adding context from the ontology (parents, children, properties) improve the results?

## Data

[OAEI Conference track](https://oaei.ontologymatching.org/2025/conference/): ontologies about conference organisation, with reference alignments made by experts.

- 16 ontologies are provided; the reference alignments cover **7** of them (Cmt, ConfTool, Edas, Ekaw, Iasted, Sigkdd, Sofsem), giving **21 test cases** (every pair of the 7).
- The data are **not included in this repository**. See *Getting the data* below.
- If you use the data, cite the OntoFarm paper indicated on the track page (Zamazal and Svátek, *The Ten-Year OntoFarm and its Fertilization within the Onto-Sphere*, Journal of Web Semantics, 2017 — please check the exact reference on the track page).

### Observations and scope decisions

- The ontologies contain **no `rdfs:label`**: entity names are taken from the end of their URI and normalised (`AuthorNotReviewer` → `author not reviewer`, `Camera_Ready_Paper` → `camera ready paper`).
- Only **named classes** are matched; anonymous classes (unions, restrictions) are ignored.
- The reference contains **305 correspondences: 259 between classes and 46 between properties**. This project evaluates **classes only** (259 correspondences). Properties are out of scope for now.
- The number of named classes found in the files differs slightly from the table of the track page for some ontologies (largest difference: Cmt, 29 against 36). The coverage check (`check_coverage.py`) shows that **every entity cited in the reference alignments is found** in the ontologies, so the evaluation is not affected. The cause of the difference was not investigated.
- The task is very imbalanced: the 21 test cases contain 98,688 possible class pairs, of which 259 are correct (about 0.26 %).

## Evaluation protocol

For each test case, the predicted pairs are compared with the reference:

- **Precision**: correct proposed pairs / proposed pairs
- **Recall**: correct proposed pairs / reference pairs
- **F1**: harmonic mean of precision and recall

Two averages are reported: **micro** (all pairs pooled, main figure) and **macro** (mean of the per-case F1). The test cases are small and unequal (from 4 to 25 class correspondences), so the micro average is more stable.

These results are **not directly comparable** with the official OAEI results, which are produced with a different evaluation framework. The comparison here is between the measures studied in this project.

## Methods

| Method | Status |
|---|---|
| Loading of ontologies and reference alignments | done |
| Coverage check of the reference alignments | done |
| Evaluation framework (precision, recall, F1, micro / macro) | in progress |
| Baseline: exact match of normalised names | in progress |
| Lexical measures (string similarity, token overlap) | planned |
| Context extraction with SPARQL | planned |
| Structural measures (neighbours in the hierarchy, properties) | planned |
| Embedding-based similarity (`nomic-embed-text` through Ollama) | planned |
| Combination of measures, with and without context | planned |
| Error analysis and small demo | planned |

## Results

No results yet. This table will be filled with measured values only.

| Method | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|
| Exact match (baseline) | — | — | — | — |
| Lexical | — | — | — | — |
| Structural | — | — | — | — |
| Embeddings | — | — | — | — |
| Combination | — | — | — | — |
| Combination + context | — | — | — | — |

## Repository structure

```
src/
  data_loading.py      read ontologies (rdflib) and reference alignments (XML)
  inspect_ontology.py  basic statistics of one ontology
  diagnose_classes.py  named / anonymous / undeclared classes of one ontology
  check_coverage.py    check that the reference entities exist in the ontologies
  normalize.py         turn entity names into plain words
  evaluation.py        precision, recall, F1
  benchmark.py         load the 21 test cases and evaluate any matcher
  baseline_exact.py    baseline: exact match of normalised names
data/raw/              downloaded data (not versioned)
```

A *matcher* is a function that takes the classes of two ontologies and returns a set of proposed pairs. Every method of the project has this form, so all of them are evaluated in the same way.

## Getting the data

1. Download `conference.zip` (link "The collection of ontologies") and `reference-alignment.zip` from the [track page](https://oaei.ontologymatching.org/2025/conference/).
2. Unzip them so that the files are in:
   - `data/raw/ontologies/` (for example `cmt.owl`, `confof.owl`, `Conference.owl`)
   - `data/raw/reference-alignment/` (21 files such as `cmt-conference.rdf`)

## Installation and usage

```bash
python -m venv .venv
source .venv/bin/activate          # Windows (Git Bash): source .venv/Scripts/activate
pip install -r requirements.txt

python src/inspect_ontology.py data/raw/ontologies/cmt.owl
python src/check_coverage.py
python src/baseline_exact.py
```

Run the commands from the root of the repository.

## Limitations

- Small ontologies from one domain (conference organisation); results may not transfer to other domains.
- Only classes are evaluated; the 46 property correspondences are not.
- Results are not comparable with official OAEI results (different evaluation framework).

## Author

Mohamed Mohamed Bowba — [github.com/mouhamedbowb](https://github.com/mouhamedbowb)

The topic was validated by the course instructor. Development was done step by step with the help of an AI assistant (Claude, Anthropic) used as a tutor; the author runs the code and is responsible for the results.
