# Inflam

![Continuous Integration build in GitHub Actions](https://github.com/DanielCollishawSchepman/python-intermediate-inflammation/workflows/CI/badge.svg?branch=main)

Inflam is a data management system written in Python that manages trial data used in clinical inflammation studies.

## Main features

Here are some key features of Inflam:

- Provide basic statistical analyses over clinical trial data
- Ability to work on trial data in Comma-Separated Value (CSV) format
- Generate plots of trial data
- Analytical functions and views can be easily extended based on its Model-View-Controller architecture

## Prerequisites

Inflam requires the following Python packages:

- [NumPy](https://www.numpy.org/) - makes use of NumPy's statistical functions
- [Matplotlib](https://matplotlib.org/stable/index.html) - uses Matplotlib to generate statistical plots

The following optional packages are required to run Inflam's unit tests:

- [pytest](https://docs.pytest.org/en/stable/) - Inflam's unit tests are written using pytest
- [pytest-cov](https://pypi.org/project/pytest-cov/) - Adds test coverage stats to unit testing

## Installation

1. Create a virtual environment: `python3 -m venv venv`.
1. Activate the virutal environment: `source ./venv/bin/activate`.
1. Install the requirements: `pip -r requirements.txt`.

## Basic usage

1. Create a file to store patient data.
    - E.g., `touch data/patients.csv`.
    - E.g., `touch data/patients.json`.
1. Adding a new patient: `python3 inflammation-analysis.py --view new-patient --patientname Bob --serializer csv data/patients.csv`.
1. Adding a new observation for that patient: `python3 inflammation-analysis.py --view new-observation --patientname Bob --observation 5 --serializer csv data/patients.csv`.

## Development

1. Run `black .` and `isort .` before committing.

## TODO

- Contributing: for those wishing to contribute to the software’s development, this is an opportunity to detail what kinds of contribution are sought and how to get involved
- Contact information/getting help: which may include things like key author email addresses, and links to mailing lists and other resources
- Credits/Acknowledgements: where appropriate, be sure to credit those who have helped in the software’s development or inspired it
- Citation: particularly for academic software, it’s a very good idea to specify a reference to an appropriate academic publication so other academics can cite use of the software in their own publications and media. You can do this within a separate CITATION text file within the repository’s root directory and link to it from the markdown
