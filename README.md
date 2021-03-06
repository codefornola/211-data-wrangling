This project will help cleanup data for [VIA LINK](https://vialink.org/), the non-profit that runs the 211 system and call centers for the New Orleans-based region of Louisiana.

## Initial setup

### install Python

You must have Python 3 installed. You can download it [here](https://www.python.org/downloads/).

> If you are using Windows, be sure to select the "Add Python to PATH" option

You can confirm it is installed correctly by running `python3 --version` in a terminal or command prompt.

### create and activate a Python virtual environment

This step is optional, but if you have more than one project using Python, it is recommended.

A [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) isolates the dependencies
of each project, which is helpful when working with mulitple projects with different depenencies (or different versions of the same dependency).

For macOS or Linux

```
python3 -m venv .venv
source .venv/bin/activate
```

For Windows

```
py -m venv env
.\env\Scripts\activate
```

> Note that you need to [activate the virutal environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
> before running a script but you only need to create the virtual envrionment once.

### install the dependencies

In Python, dependencies are often installed using [pip](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-pip)

You can install all the dependencies for this project by running:

```
pip install -r requirements.txt
```

## Running the scripts

The basic format looks like `python cleanup.py script_name --inputfile1 ~/path/to/input.csv`

For example:

```
# the keep-calm-with-covid script only requires one input file
python cleanup.py --debug keep-calm-with-covid --input "/tmp/VL 4.29 Call Report.csv"

# the all-covid-calls script requires 2 files
python cleanup.py --debug all-covid-calls --vialink-input ~/Downloads/VL\ 4.29\ Disaster\ Call\ Report\ .csv --232-input ~/Downloads/232-HELP.csv"
```

If you want to see the basic usage you can run `python cleanup.py` and for a specifc command you can use the `--help` flag

```
python cleanup.py all-covid-calls --help
```

> Also, you can use the `--debug` flag to view debug logs
