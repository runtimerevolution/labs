# labs

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Runtime Labs

## Getting Started

Here's the steps to setup the project locally:

1. poetry shell
2. poetry install
3. make setup
4. make tests

# Troubleshooting

## PyICU

Please install pkg-config on your system or set the ICU_VERSION environment
variable to the version of ICU you have installed

If you see this error, when installing the package PyICU, you can solve the issue with these steps:

1. brew install pkg-config icu4c;
2. brew info icu4c;
3. Look for the lines that export the path for icu to the PATH environment variable and add them to you your bashrc (or zshrc, whichever you use);
4. Rerun poetry install again and there should be no error.
