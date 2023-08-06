# jrpytests

## Overview

This package contains functions for CI testing of JR python packages and was created using the poetry python package, for more details see

[https://github.com/sdispater/poetry](https://github.com/sdispater/poetry).

jrpytests allows: 

* to run pytest,
* to check coding style (via flake8) in python files, 
* to extract python chunks from Rmd files and check their coding style,
* to check if a directory 'vignettes' exists in appropriate folder and,
* to count pdf files in 'vignettes' and compare to number of Rmd files.

The flake8 configuration file is stored in this package, see

jrpytests/flake8\_config.ini.

## Basic usage

Import the package using

`import jrpytests`.

Run pytest

`jrpytests.runpytests()`.

Run flake8 in python files

`jrpytests.runflake8pythonfiles()`.

Run flake8 in Rmd python chunks

`jrpytests.runflake8rmdpychunks()`.

Check 'vignettes' and number of pdf files in it

`jrpytests.checkvignettespdffiles()`.
