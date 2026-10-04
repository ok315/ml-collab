# MLOps Collaborative Project

## Project Overview

This repository contains a collaborative Machine Learning Operations (MLOps) project developed by DataMinds. The project focuses on building a reproducible machine learning workflow for predicting customer churn using the Telco Customer Churn dataset.

## Team

* **Osama** — Team member
* **Abdurrahman** — Team member

## Project Objectives

* Develop a machine learning model for customer churn prediction.
* Organize the project using a maintainable directory structure.
* Implement version control and collaborative Git workflows.
* Track datasets and experiments using appropriate MLOps tools.
* Establish code quality checks and automated testing.
* Configure continuous integration with GitHub Actions.
* Support reproducible training and model release.

## Repository Structure

```text
ml-collab/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── tests/
├── reports/
│   └── figures/
├── .github/
│   └── workflows/
└── docs/
```

## Technology Stack

* Python
* Git and GitHub
* DVC
* pandas and scikit-learn
* pytest
* pre-commit
* GitHub Actions

## Project Status

Initial repository setup and project structure.

## Dataset

The project will use the Telco Customer Churn dataset. Dataset source, license, and preparation details will be documented as the project progresses.

## Collaboration

Team members will collaborate through Git branches, pull requests, code reviews, and documented project workflows.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

If `dvc pull` complains about S3 support, run `pip install "dvc[s3]"`.

## Get the data

Data and models are versioned with DVC; the remote is DagsHub. Add your own
DagsHub token locally. It is stored in `.dvc/config.local` and is never committed:

```powershell
dvc remote modify --local storage access_key_id <your-dagshub-token>
dvc remote modify --local storage secret_access_key <your-dagshub-token>
dvc pull
```

## Run the pipeline

```powershell
dvc repro          # prepare -> train -> evaluate, writes metrics.json
dvc repro --force  # re-run every stage, e.g. to check reproducibility
```

All settings (seed, split ratio, model hyperparameters) live in `params.yaml`.

## Run experiments

```powershell
dvc exp run --temp -n <name> --set-param model.max_depth=6
dvc exp show
```

`--temp` runs the experiment in a temporary copy, so your working folder stays clean.

## Project layout

| Path | Purpose |
|---|---|
| `params.yaml` | seed, split ratio, model hyperparameters |
| `dvc.yaml`, `dvc.lock` | pipeline stages and the recorded hashes |
| `metrics.json` | latest evaluation metrics |
| `src/data/` | `prepare.py` (clean and split), `validate.py` (checks) |
| `src/models/` | `train.py`, `evaluate.py` |
| `src/config.py` | loads `params.yaml` |
| `data/raw/` | raw dataset, tracked by DVC, not by Git |
| `models/` | trained model, tracked by DVC |

## Workflow

Nobody pushes directly to `dev`, `staging` or `main`. Work happens on `feat/`,
`data/` and `exp/` branches and reaches `dev` through reviewed pull requests.