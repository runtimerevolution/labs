# labs

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Runtime Labs


## Start working on the project

In order to start working on the project you just have to run `make start` and you are ready to go!

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for labs
│                         and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── labs                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes labs a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```

--------

## Use of Pixi in Runtime Labs project

1. **`pixi init .`**: Initializes Pixi for the current directory.
2. **`pixi shell`**: Opens a Pixi shell with the Pixi-managed Python version.
3. **`python --version`**: Checks the Python version, which will show your current python version.
4. **`pixi add python==3.11.9`**: Adds Python version **3.11.9** to the project.
5. **`python --version`**: If you check the Python version, now it's **3.11.9**.
6. **`pixi add python==3.12.2`**: If for some reason you made a mistake you can add a new version.
7. **`python --version`**: If you check the Python version again, now it's **3.12.2**.
8. **`which python`**: This will show you the path to the Python interpreter.
9. **`exit`**: Exits the Pixi shell.
10. **`python --version`**: Now, if you check the Python version outside the Pixi shell, it's back to the version you started with. 

