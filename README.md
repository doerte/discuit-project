## Badges

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/doerte/discuit-project) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/doerte/discuit-project)](https://github.com/doerte/discuit-project) |
| (3/5) community registry           | <!-- [![RSD](https://img.shields.io/badge/rsd-discuit-00a3e3.svg)](https://www.research-software.nl/software/<replace-with-name>) [![workflow pypi badge](https://img.shields.io/pypi/v/<replace-with-name>.svg?colorB=blue)](https://pypi.python.org/project/<replace-with-name>/) -->|
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7671856.svg)](https://doi.org/10.5281/zenodo.7671856) |
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>/badge)](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **Other best practices**           | &nbsp; |
| Static analysis                    | [![workflow scq badge](https://sonarcloud.io/api/project_badges/measure?project=doerte_discuit-project&metric=alert_status)](https://sonarcloud.io/dashboard?id=doerte_discuit-project) |
| Coverage                           | [![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=doerte_discuit-project&metric=coverage)](https://sonarcloud.io/dashboard?id=doerte_discuit-project) |
| Documentation                      | <!-- [![Documentation Status](https://readthedocs.org/projects/discuit-project/badge/?version=latest)](https://<replace-with-name>.readthedocs.io/en/latest/?badge=latest) --> |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/doerte/discuit-project/actions/workflows/build.yml/badge.svg)](https://github.com/doerte/discuit-project/actions/workflows/build.yml) |
| Citation data consistency               | [![cffconvert](https://github.com/doerte/discuit-project/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/doerte/discuit-project/actions/workflows/cffconvert.yml) |
| SonarCloud                         | [![sonarcloud](https://github.com/doerte/discuit-project/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/doerte/discuit-project/actions/workflows/sonarcloud.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/doerte/discuit-project/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/doerte/discuit-project/actions/workflows/markdown-link-check.yml) |

## About Discuit

Discuit is a **D**ynamic **i**tem **s**et **c**lustering **UI** **t**ool (with the UI part yet to come)

Discuit can split datasets (e.g. words defined by several variables) into subsets that are as comparable as possible.

The package takes a csv file as input and generates a defined number of matched sets for a given number of continuous and categorical variables. One of the categorical variables can be selected to be split absolutely even across sets. Discuit generates the following output:
- csv file ammended with the set membership for each item
- txt file that reports on the outcomes of statistics tests

In the future, this will be integrated in an GUI. 

The project setup is documented in [project_setup.md](project_setup.md).

## Installation

Discuit is available on PyPI!

```bash
pip install discuit
```

Or install the latest development version directly from GitHub:

```console
git clone git@github.com:doerte/discuit-project.git
cd discuit-project
python3 -m pip install .
```

<!-- ## Documentation

Include a link to your project's full documentation here. --> 

## Using Discuit
In the terminal, run Discuit with the following command:
discuit "name of input file" [number of desired sets] --columns l/c/n/a/d --runs [desired number of runs]

Example: discuit example/input.csv 2 --columns l a n c n d --runs 3

This will run Discuit with the [provided testfile](example/input.csv) and create 2 subsets. 
The columns in the file are identified as "label", "categorical", "numerical", "absolute", "numerical" 
and "disregard" (in that order). The program will run 3 times (and create 3 output files).

### Required input
The input file needs to be a .csv file with a first line containing headings followed by rows that represent the different items. Each column specifies one variable. 

When launching the script, please specify per column what kind a data the script should expect: 
- (l)abel: just a label, will not be taken into consideration, could be the itemname or itemnumber. This can only be assigned once. 
- (n)umerical: a numerical variable, such as frequency or AoA, 
- (c)ategorical: a categorical variable, such as "transitivity" or "accuracy", 
- (a)bsolute: this needs to be perfectly divided between sets. This can only be assigned once. 
- (d)isregard: a column that does not need to be taken into account for the split, but contains other information you have in the same file.

The package will try maximally 20 times to come-up with a good split. If it doesn't it will give up and output it's last try. You can always run it again. Often it will succeed eventually. If not, consider dropping variables.

If you run the script without specifying --columns, you will be asked what you want per column. If you don't specify the desired number of runs, it will generate 1 output file.

### Missing data
If you choose an "absolute split variable", this variable cannot have missing data. The program will exit if it does. 
For categorical variables, a dummy category is created that holds the items with missing data. For numerical variables,
missing data is replaced with the average of this variable.
If you prefer a different approach, please prepare your input file in a way that does not include missing data.

## Contributing

If you want to contribute to the development of Discuit,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
