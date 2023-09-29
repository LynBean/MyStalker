> [!IMPORTANT]
> Only for Malaysian, foreigners are not able to use this program. Unless you use VPN to connect to Malaysia.

[![LICENSE](https://img.shields.io/github/license/LynBean/MyStalker?label=LICENSE)](https://github.com/LynBean/MyStalker/blob/main/LICENSE)

`mystalker` is a command-line application written in Python that can retrieve students details such as NRIC, Student Name and others.

##### _Use responsibly. For Educational Purposes Only_

---

> [!IMPORTANT]
> Required Python 3.10 or above

### To install MyStalker

```bash
$ pip install "git+https://github.com/LynBean/MyStalker@main"
```

If you met installation error, or the program cannot be called after installation succeeded, you may try to reinstall the package but using administrator terminal

### To update MyStalker

```bash
$ pip install "git+https://github.com/LynBean/MyStalker@main" --upgrade
```

### Alternatively, you can clone the project and run the following command to install

Make sure you cd into the _MyStalker-main_ folder before performing the command below.

```bash
$ pip install .
```

---

### Simply Start

```bash
$ mystalker
```

### Useful tips

> [!NOTE]
> For getting the state code, district code and school code,
> you may refer to the file "schools.csv" in the repository

```bash
# Range of digits to search
$ mystalker --loop-digit-start=0 --loop-digit-stop=3000

# Specify the state where the student was born
$ mystalker --birth-state-code=08

# Difference between `current-living-state-code` and `birth-state-code`
# is that `current-living-state-code` is NOT fixed in NRIC generation,
# but `birth-state-code` does.
# So a single NRIC can go through multiple states to have more accurate
# results.
$ mystalker --birth-state-code=08 --current-living-state-code=12

# You may also specify `district-code` or `school-code` to have a smaller
# range in searching
$ mystalker --district-code=J010 --school-code=JBA0001

# NEW FEATURE CHECKPOINT!!
# Use `-c` to autogenerate checkpoint file and autoresume during next run.
# Or `-n` to specify the checkpoint filepath that you preffered.
$ mystalker -c
$ mystalker -n "C://User/user/mystalker.checkpoint"
```

### See where is the data stored

```bash
mystalker --where
```

## Options

---

```bash
Usage: mystalker [-h] [-v] [-w] [--database-renew-interval DAYS] [--loop-digit-start DIGIT] [--loop-digit-stop DIGIT] [--birth-state-code STATE_CODE] [--current-living-state-code STATE_CODE]
                 [--district-code DISTRICT_CODE] [--school-code SCHOOL_CODE] [--birth-date YYMMDD] [--loop-birth-date-start YYMMDD] [--loop-birth-date-stop YYMMDD] [--gender GENDER] [-c]
                 [-f FILEPATH] [--nogui]
Options:
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

  --district-code DISTRICT_CODE
                        Specify the district where the student is currently living.

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

  --nogui               Disable GUI.
```
