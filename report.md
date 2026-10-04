# REPORT: Telco Customer Churn, Git and DVC collaboration

## 1. Team, roles, dataset, starter code
- Abdurrahman: Model owner (training pipeline, configs, experiments)
- Osama: Data owner, and Platform owner (split between us in a team of two)
- Dataset: Telco Customer Churn (Kaggle) 
- Starter code source: <TODO describe honestly: where it came from, with a link, and
  any help you used>

## 2. Reproducibility table (released model)

| Item | Value |
|---|---|
| Commit SHA | `ffb0ff25ccbed18bb51a726f1eb4245ff0985815` |
| params.yaml values | `random_state=42, test_size=0.2, algorithm=random_forest, n_estimators=100, max_depth=6, class_weight=balanced` |
| Data .dvc md5 | `3b0bfab28a8101b4e4fdd08025a5c235` |
| dvc.lock | `dvc.lock` |
| Seed | `42` |
| Final metrics | `accuracy=0.7466, precision=0.5147, recall=0.7968, f1=0.6254, roc_auc=0.84` |

## 3. Experiments
Selection rule: highest ROC-AUC, F1 as tie-breaker. Runs used a fixed seed and split.

| Experiment | max_depth | n_estimators | accuracy | precision | recall | f1 | roc_auc |
|---|---|---|---|---|---|---|---|
| baseline | 10 | 100 | 0.7537 | 0.5254 | 0.7460 | 0.6166 | 0.8376 |
| depth-4 | 4 | 100 | 0.7289 | 0.4933 | 0.7834 | 0.6054 | 0.8350 |
| depth-6 (winner) | 6 | 100 | 0.7466 | 0.5147 | 0.7968 | 0.6254 | 0.8400 |
| depth-14 | 14 | 100 | 0.7587 | 0.5360 | 0.6765 | 0.5981 | 0.8266 |

Why depth-6: best ROC-AUC, F1 and recall, with a consistent trend across the sweep. The
ROC-AUC gain (+0.0024) is small and within noise, so this is a judgment call.
Depth-14 was abandoned because it overfits (see section 4).
Osama's experiments: TODO

## 4. Links
- Data-update PR: TODO
- Conflict-resolution PR: TODO
- A "changes requested" review: TODO
- Release PRs (dev to staging, staging to main): TODO
- Abandoned exp/ branch: https://github.com/ok315/ml-collab/tree/exp/abdurrahman-tuning

## 5. Screenshots

### Blocked large file

![Blocked large file](docs/screenshots/Blocked-Large-File.PNG)

### Blocked secret

![Blocked secret](docs/screenshots/Blocked-Secrets.png)

### Failing CI check

![Failing CI check](docs/screenshots/Failed-CI-Check.png)

### Passing CI check

![Passing CI check](docs/screenshots/passing-CI-Check.png)

## 6. Retrospective
What broke:
- Windows blocked venv activation; some work started on the wrong branch
- Dependencies were installed into the global Python before using a venv
- Plain dvc exp run kept params from the previous run, so one run changed two things
- dvc.lock recorded CRLF hashes from Windows; Linux would hash them differently
- ruff.toml was not committed, which would have failed CI
- Some pushes reached dev and main before branch protection was on
What we added to CONTRIBUTING.md because of it: TODO

## 7. Contributions
- Abdurrahman: TODO write at the end, from your own PRs and reviews
- Osama: TODO



https://github.com/ok315/ml-collab/pull/9#top