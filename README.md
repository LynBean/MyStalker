# Only for Malaysian

[![LICENSE](https://img.shields.io/github/license/LynBean/MyStalker?label=LICENSE)](https://github.com/LynBean/MyStalker/blob/main/LICENSE)

`mystalker` is a command-line application written in Python that can retrieve students details such as NRIC, Student Name and others.

##### _Use responsibly. For Educational Purposes Only_

## Install

---

**Only for Python version >= 3.10**

### To install MyStalker

```bash
pip install "git+https://github.com/LynBean/MyStalker@main"
```
*If you met installation error, or the program cannot be called after installation succeeded, you may try to reinstall the package but using administrator terminal*
### To update MyStalker

```bash
pip install "git+https://github.com/LynBean/MyStalker@main" --upgrade
```

### Alternatively, you can clone the project and run the following command to install

Make sure you cd into the _MyStalker-main_ folder before performing the command below.

```bash
pip install .
```

## Usage

---

### Simply Start

```bash
mystalker
```

### For faster searching, you can use the following options

If result not good for you, you can increase the range

```bash
mystalker --loop-digit-start=0 --loop-digit-stop=3000
```

### See where is the data stored

```bash
mystalker --where
```

## Options

---

```
Usage: mystalker [-h] [-v] [-w] [--database-renew-interval DAYS] [--loop-digit-start DIGIT] [--loop-digit-stop DIGIT] [--birth-state-code STATE_CODE]
                 [--current-living-state-code STATE_CODE] [--school-code SCHOOL_CODE] [--birth-date YYMMDD] [--loop-birth-date-start YYMMDD] [--loop-birth-date-stop YYMMDD]
                 [--gender GENDER] [-c] [-f FILEPATH]

options:
  -h, --help            show this help message and exit

  -v, --version         show program's version number and exit

  -w, --where           Specify the directory to store the database.

  --database-renew-interval DAYS
                        Specify the database renew interval in days.

  --loop-digit-start DIGIT
                        Specify the starting range for digits.

  --loop-digit-stop DIGIT
                        Specify the stopping range for digits.

  --birth-state-code STATE_CODE
                        Specify the state where the student was born.

  --current-living-state-code STATE_CODE
                        Specify the state where the student is currently living.

  --school-code SCHOOL_CODE
                        Specify the school code.

  --birth-date YYMMDD   Specify the student's birth date in YYMMDD format.

  --loop-birth-date-start YYMMDD
                        Specify the starting range for birth date.

  --loop-birth-date-stop YYMMDD
                        Specify the stopping range for birth date.

  --gender GENDER       Specify the gender of the student.

  -c, --checkpoint      Enable checkpoint resuming mechanism.

  -f FILEPATH, --checkpoint-file FILEPATH
                        Specify the checkpoint filepath.

```
