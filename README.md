
# Only for Malaysian

[![LICENSE](https://img.shields.io/github/license/LynBean/MyStalker?label=LICENSE)](https://github.com/LynBean/MyStalker/blob/main/LICENSE)

`mystalker` is a command-line application written in Python that can retrieve students details such as NRIC, Student Name and others.

##### *Use responsibly. For Educational Purposes Only*

## Install

-------

**Only for Python version >= 3.3**

### To install MyStalker

```bash
pip install 'git+https://github.com/LynBean/MyStalker@main'
```

### To update MyStalker

```bash
pip install 'git+https://github.com/LynBean/MyStalker@main' --upgrade
```

### Alternatively, you can clone the project and run the following command to install

Make sure you cd into the *MyStalker-main* folder before performing the command below.

```bash
pip install .
```

## Usage

-----

### Simply Start

```bash
mystalker
```

### For faster searching, you can use the following options

If result not good for you, you can increase the range

```bash
mystalker --digit-start=0 --digit-stop=3000
```

### See where is the data stored

```bash
mystalker --where
```

## Options

-----

```
Usage: mystalker [-h] [-v] [-w] [--print-flush] [--instant-start] [--tabulate-format FORMAT] [--database-validate-days DAYS] [--digit-start INTEGER] [--digit-stop INTEGER] [--cl-state-code CODE] [--b-state-code CODE] [--school-code CODE] [--birth-date YYMMDD] [--birth-date-start YYMMDD] [--birth-date-end YYMMDD] [--gender GENDER] [--debug]

Retrieve Student Details from any given details

Options:

  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit

  -w, --where           Show where is the data stored

  --print-flush         Whether to forcibly flush the stream

  --instant-start       Skip the menu and start immediately

  --tabulate-format FORMAT
                        The format to use for tabulating the data

  --database-validate-days DAYS
                        How many days can a DataBase.csv be valid, If 7, it will get update if exceeds 7 days count from the last update

  --digit-start INTEGER
                        Generate NRIC last 4 digits start from this number

  --digit-stop INTEGER  Generate NRIC last 4 digits stop at this number

  --cl-state-code CODE  State Code of the State where the student is living currently

  --b-state-code CODE   State Code of the State where the student is born

  --school-code CODE    School Code of the School

  --birth-date YYMMDD   Birth Date of the Student

  --birth-date-start YYMMDD
                        Start date of a looping birth date

  --birth-date-end YYMMDD
                        End date of a looping birth date

  --gender GENDER       Gender of the Student

  --debug               Enable Debug Mode


How to start:

$ mystalker

Tips:
For faster searching, you can use the following options:

$ mystalker --digit-stop 3000

Note for last 4 digits information:
Person born prior and in the year 1999 will have the number started with 5## or 6## or 7## while a person born after and in the year 2000 will have the number started with 0##

See where is the data stored:

$ mystalker --where

If you don't know what is your STATE CODE or SCHOOL CODE, please refer to the following link:
https://github.com/LynBean/MyStalker/blob/main/Example%20Database/DataBase.csv
```
