This project will help cleanup data for [VIA LINK](https://vialink.org/), the non-profit that runs the 211 system and call centers for the New Orleans-based region of Louisiana. 

## Initial setup

### install Python 

You must have Python 3 installed.  You can download it [here](https://www.python.org/downloads/).

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

TBD - but probably something like this:

```
python cleanup /path/to/file1.xlsx /path/to/file2.xlsx
```
