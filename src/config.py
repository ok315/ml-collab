from pathlib import Path

import yaml

# Find the repository root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to the experiment configuration
PARAMS_PATH = PROJECT_ROOT / "params.yaml"


def load_params():
    """Load project parameters from params.yaml."""
    with PARAMS_PATH.open("r", encoding="utf-8") as file:
        params = yaml.safe_load(file)

    return params


if __name__ == "__main__":
    config = load_params()
    print(config)
