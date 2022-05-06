
Malaysian Identity Scraper
=================
[![LICENSE](https://img.shields.io/badge/LICENSE-GPL--3.0-orange)](https://github.com/victoryy2003/Malaysian-Identity-Scraper/blob/main/LICENSE) [![PythonVersion](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/)

`MYScraper` is a command-line application written in Python that scrapes users identity including his/her Identity Numbers, Full name, Place of birth / Area / District of the user. 

*Use responsibly. For Educational Purposes Only*


Install
-------
To install MYScraper :
```bash
$ pip install MYScraper
```

To update MYScraper :
```bash
$ pip install MYScraper --upgrade
```
Alternatively, you can clone the project and run the following command to install:
Make sure you cd into the *Malaysian-Identity-Scraper-main* folder before performing the command below.
```
$ pip install -e .
```


Usage
-----

To scrape a user :
```bash
$ MYScraper
```

There are Four options need to be fill in :
```
$ Please enter the birth date : (031231) 
$ Please enter the place of birth : (13)(If no just keep it blank) 
$ Please enter the gender : (Female)(If no just keep it blank) 
$ Please enter the school code : (YCC4102)(If no just keep it blank) 
```
*Providing Birth date is compulsary*

The resulting directory structure will be :
```
Current Directory
├── Database.json << "Don't touch this file"
├── HereYouGo.json << "Final result in JSON format"
└── HereYouGo.txt << "Final result in TEXT format"
```

Develop
-------

Clone the repo and create a virtualenv 
```bash
$ virtualenv venv
$ source venv/bin/activate
$ python setup.py develop
```

[//]: # (Running Tests)
[//]: # (-------------)

[//]: # (```bash)
[//]: # ($ python setup.py test)

[//]: # (# or just )

[//]: # ($ nosetests)
[//]: # (```)

Contributing
------------

1. Check the open issues or open a new issue to start a discussion around
   your feature idea or the bug you found
2. Send a pull request

License
-------
GNU GENERAL PUBLIC LICENSE

Version 3, 29 June 2007
