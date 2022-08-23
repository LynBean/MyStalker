
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

```bash
   -h, --help           show this help message and exit
   --version            show program's version number and exit
   -p, --print-flush    Whether to forcibly flush the stream
   -f FORMAT, --tabulate-format FORMAT
                        The format to use for tabulating the data
   -d DAYS, --database-validate-days DAYS
                        How many days can a DataBase.csv be valid, If 7, it will get update if exceeds 7 days count from the last update
   -s INTEGER, --digit-start INTEGER
                        Generate NRIC last 4 digits start from this number
   -e INTEGER, --digit-stop INTEGER
                        Generate NRIC last 4 digits stop at this number
   -w, --where          Show where is the data stored
```
