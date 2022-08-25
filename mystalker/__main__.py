
import argparse
import functools
import os
import pandas as pd
import platform
import re
import requests
import sys
import textwrap
import threading
import time
import traceback
import urllib3

from bs4 import BeautifulSoup as bs
from colorama import Fore, Back, Style
from datetime import datetime, timedelta
from random import randint
from tabulate import tabulate

from .constants import *
from .dataframe import DataFrame as DF
from .path import Path


class Spinner:
    busy = False
    delay = 0.1

    def spinning_cursor(self):
        while 1:
            for cursor in self.word_list:
                yield cursor

    def __init__(
        self,
        word_list: list,
        delay: float = None
        ):

        self.spinner_generator = self.spinning_cursor()
        self.word_list = word_list
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            print(next(self.spinner_generator), flush = True, end = '\r')
            time.sleep(self.delay)

    def __enter__(self):
        self.busy = True
        threading.Thread(target = self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False


def get_version() -> str:
    SRC = os.path.abspath(os.path.dirname(__file__))
    PATH = os.path.join(SRC, '__init__.py')

    with open(PATH, encoding = 'UTF-8') as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)


def cls(
    art: bool = True,
    fore_color: Fore = Fore.CYAN
    ) -> None:

    os.system('cls' if platform.system() == 'Windows' else 'clear')
    if art is True:
        print(
            '',
            Fore.RED     + '\t███╗░░░███╗██╗░░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░██╗███████╗██████╗░',
            Fore.YELLOW  + '\t████╗░████║╚██╗░██╔╝██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░██╔╝██╔════╝██╔══██╗',
            Fore.GREEN   + '\t██╔████╔██║░╚████╔╝░╚█████╗░░░░██║░░░███████║██║░░░░░█████═╝░█████╗░░██████╔╝',
            Fore.CYAN    + '\t██║╚██╔╝██║░░╚██╔╝░░░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██╔═██╗░██╔══╝░░██╔══██╗',
            Fore.BLUE    + '\t██║░╚═╝░██║░░░██║░░░██████╔╝░░░██║░░░██║░░██║███████╗██║░╚██╗███████╗██║░░██║',
            Fore.MAGENTA + '\t╚═╝░░░░░╚═╝░░░╚═╝░░░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝\n\n',
            fore_color
            )


def digits_generator(
    gender: str = None,
    start: int = 0,
    stop: int = 10000
    ) -> list:

    digits = []

    try:
        stop = 10000 if stop >= 10000 else stop

        if gender.upper() in ('MALE') and gender != '':
            start = start + 1 if start % 2 == 0 else start
            for x in range(start, stop, 2):

                digits.append(str(x).zfill(4))

        elif gender.upper() in ('FEMALE') and gender != '':
            start = start + 1 if start % 2 == 1 else start
            for x in range(start, stop, 2):

                digits.append(str(x).zfill(4))

        else:
            raise ValueError('Not in MALE or FEMALE')

    except (AttributeError, ValueError):
        for x in range(start, stop):

            digits.append(str(x).zfill(4))

    return digits


def valid_date(
    date,
    is_argparse: bool = False
    ) -> bool | str:

    try:
        if len(date) != 6:
            raise ValueError

        datetime.strptime(date, '%y%m%d')

        if is_argparse is True:
            return date

        return True

    except ValueError:

        if is_argparse is True:
            raise argparse.ArgumentTypeError('Date must be in YYMMDD format')

        return False


def date_generator(
    start_date: str,
    end_date: str
    ) -> list:

    default_start_date = '000101'
    default_end_date = datetime.now()

    start_date = datetime.strptime(start_date if start_date is not None else default_start_date, '%y%m%d')
    end_date = datetime.strptime(end_date, '%y%m%d') if end_date is not None else default_end_date
    df_date = pd.date_range(start_date, end_date - timedelta(days = 1), freq = 'd')
    date_list = [pd.to_datetime(date).strftime('%y%m%d') for date in df_date.values]

    return date_list


def nric_valid(
    date_birth: str,
    state_code: str,
    digit: str,
    school_code: str = None
    ) -> bool:

    session = requests.Session()
    session.headers.update(
        USER_AGENT
        )

    while True:
        try:
            html_response = session.get(
                '{0}?nokp={1}{2}{3}'.format(
                    PAPAR_CARIAN_URL,
                    date_birth,
                    state_code,
                    digit
                    ),
                verify = False
                )
            if html_response.status_code == 200:
                break
        except NETWORK_ERROR_EXCEPTIONS:
            print(Back.YELLOW + Fore.BLACK + '\t ConnectionTimeout: Retrying ... ' + Style.RESET_ALL, end = '\r')
            time.sleep(randint(1, 5))
            continue

    if 'Tidak Wujud' in html_response.text:
        return False

    if school_code is None:
        return True

    while True:
        try:
            html_response = session.get(
                '{0}?nokp={1}{2}{3}&kodsek={4}'.format(
                    PAPAR_CARIAN_PELAJAR_URL,
                    date_birth,
                    state_code,
                    digit,
                    school_code
                    ),
                verify = False
                )
            if html_response.status_code == 200:
                break
        except NETWORK_ERROR_EXCEPTIONS:
            print(Back.YELLOW + Fore.BLACK + '\t ConnectionTimeout: Retrying ... ' + Style.RESET_ALL, end = '\r')
            time.sleep(randint(1, 5))
            continue

    if 'Tidak Wujud' in html_response.text:
        return False


def retrieve_details(
    date_birth: str,
    state_code: str,
    digit: str,
    school_code: str
    ) -> dict:

    session = requests.Session()
    session.headers.update(
        USER_AGENT
        )

    while True:
        try:
            html_response = session.get(
                '{0}?nokp={1}{2}{3}&kodsek={4}'.format(
                    PAPAR_CARIAN_PELAJAR_URL,
                    date_birth,
                    state_code,
                    digit,
                    school_code
                    ),
                verify = False
                )
            if html_response.status_code == 200:
                break
        except NETWORK_ERROR_EXCEPTIONS:
            print(Back.YELLOW + Fore.BLACK + '\t ConnectionTimeout: Retrying ... ' + Style.RESET_ALL, end = '\r')
            time.sleep(randint(1, 5))
            continue

    if ('Tidak Wujud' in html_response.text):
        return None

    while True:
        try:
            html_response = session.get(
                IBUBAPA_SEMAK_URL,
                verify = False
            )
            if html_response.status_code == 200:
                break
        except NETWORK_ERROR_EXCEPTIONS:
            print(Back.YELLOW + Fore.BLACK + '\t ConnectionTimeout: Retrying ... ' + Style.RESET_ALL, end = '\r')
            time.sleep(randint(1, 5))
            continue

    soup = bs(html_response.text, 'lxml')
    student_name = soup.find(
        lambda x: x.text.strip() == 'NAMA MURID'
        ).find_next(
            'td'
            ).find_next(
                'td'
                ).text.strip()

    df_school = df.loc[df['School Code'] == school_code]

    state_code = df_school['State Code'].values[0]
    state_name = df_school['State Name'].values[0].split(' - ')[1]
    district_code = df_school['District Code'].values[0]
    district_name = df_school['District Name'].values[0].split(' - ')[1]
    school_name = df_school['School Name'].values[0]

    return {
        'State Code': [state_code],
        'State Name': [state_name],
        'District Code': [district_code],
        'District Name': [district_name],
        'School Code': [school_code],
        'School Name': [school_name],
        'Student Name': [student_name],
        'Student NRIC': [str(date_birth + state_code + digit)]
    }


def _main(
    print_flush: bool = False,
    tabulate_format: str = 'psql',
    database_validate_days: int = 7,
    instant_start: bool = False,
    digit_start: int = 0,
    digit_stop: int = 10000,
    school_code: str = None,
    b_state_code: str = None,
    cl_state_code: str = None,
    birth_date: str = None,
    birth_date_start: str = None,
    birth_date_end: str = None,
    gender: str = None,
    ) -> None:


    # -------------------------------------------------------------------------
    #                           INITIALIZE VARIABLES

    global tabulate, print
    tabulate = functools.partial(tabulate, headers = 'keys', tablefmt = tabulate_format, showindex = False, missingval = 'None')
    print = functools.partial(print, flush = print_flush, sep = '\n')

    global df_valid_student
    df_valid_student = pd.DataFrame()
    df_option = pd.DataFrame(
        {
            'Date of Birth': [None],
            'Gender': [None],
            'Born State Code': [None],
            'Current Living State Code': [None],
            'School Code': [None]
        }
    )

    df_option.loc[0, 'Date of Birth'] = birth_date
    start_date = birth_date_start
    end_date = birth_date_end
    df_option.loc[0, 'Gender'] = gender
    df_option.loc[0, 'Born State Code'] = b_state_code
    df_option.loc[0, 'Current Living State Code'] = cl_state_code
    df_option.loc[0, 'School Code'] = school_code


    cls()
    # -------------------------------------------------------------------------
    #                           LOAD DATABASE

    global df
    with Spinner(['\t' + Fore.YELLOW + x + Back.LIGHTBLACK_EX + Fore.WHITE + '\t Getting latest database, this might take a while :D \t\t\t\t' + Style.RESET_ALL for x in '⣷⣯⣟⡿⢿⣻⣽⣾'],
                 delay = 0.1):
        df = DF().pull_csv(
            days_ago = database_validate_days,
        )


    # -------------------------------------------------------------------------
    #                            PROMPTS

    def set_date_birth():
        date_birth = input(Back.YELLOW + Fore.BLACK + '\t Enter date of birth (YYMMDD): ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)

        if valid_date(date_birth) is False:
            input(Back.RED + Fore.BLACK + '\n\t Invalid Date of Birth' + Style.RESET_ALL)
            return

        df_option.loc[0, 'Date of Birth'] = date_birth

    def set_gender():
        gender = input(Back.YELLOW + Fore.BLACK + '\t Enter gender (MALE/FEMALE): ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)

        try:
            if gender == '':
                raise ValueError
            elif gender.upper() in ('MALE', 'FEMALE'):
                pass
            else:
                raise ValueError
        except (AttributeError, ValueError):
            input(Back.RED + Fore.BLACK + '\n\t Invalid Gender' + Style.RESET_ALL)
            return

        df_option.loc[0, 'Gender'] = gender.upper()

    def set_b_state_code():
        b_state_code = input(Back.YELLOW + Fore.BLACK + '\t Enter born state code (2 digits): ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)
        if b_state_code == '' or b_state_code not in df['State Code'].values:
            input(Back.RED + Fore.BLACK + '\n\t Invalid State Code' + Style.RESET_ALL)
            return

        df_option.loc[0, 'Born State Code'] = b_state_code

    def set_cl_state_code():
        cl_state_code = input(Back.YELLOW + Fore.BLACK + '\t Enter current living state code (2 digits): ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)
        if cl_state_code == '' or cl_state_code not in df['State Code'].values:
            input(Back.RED + Fore.BLACK + '\n\t Invalid State Code' + Style.RESET_ALL)
            return

        df_option.loc[0, 'Current Living State Code'] = cl_state_code

    def set_school_code():
        school_code = input(Back.YELLOW + Fore.BLACK + '\t Enter school code: ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)
        if school_code == '' or school_code.upper() not in df['School Code'].values:
            input(Back.RED + Fore.BLACK + '\n\t Invalid School Code' + Style.RESET_ALL)
            return

        df_option.loc[0, 'School Code'] = school_code.upper()


    while instant_start is False:
        cls()
        print(
            tabulate(
                df_option,
                ),
            '\n\tThis program has designated to search through all posibilities of NRIC.',
            '\tPlease make sure you have entered the correct information.',
            '\tIf you are not sure, you may leave it blank.\n',
            '\t1. Provide Date of Birth',
            '\t2. Provide Gender',
            '\t3. Provide Born State Code',
            '\t4. Provide Current Living State Code',
            '\t5. Provide School Code',
            '',

            '\tS. Lesgo!',
        )

        option_dict = {
            '1': set_date_birth,
            '2': set_gender,
            '3': set_b_state_code,
            '4': set_cl_state_code,
            '5': set_school_code
        }

        option = input(Back.YELLOW + Fore.BLACK + '\n\t Enter your option: ' + Back.BLUE + Fore.BLACK + Style.RESET_ALL)

        if option.upper() == 'S':

            if df_option['Date of Birth'].values[0] is None:

                while True:
                    start_date = input(Back.RED + Fore.BLACK + '\n\t Enter a starting date (default: 000101)(You may leave it blank): ' + Style.RESET_ALL)
                    if valid_date(start_date) is True:
                        break
                    print(Back.RED + Fore.BLACK + '\n\t Must be in format YYMMDD ' + Style.RESET_ALL)

                while True:
                    end_date = input(Back.RED + Fore.BLACK + '\n\t Enter an ending date (default: ' + datetime.now().strftime('%y%m%d') + ')(You may leave it blank): ' + Style.RESET_ALL)
                    if valid_date(end_date) is True:
                        break
                    print(Back.RED + Fore.BLACK + '\n\t Must be in format YYMMDD ' + Style.RESET_ALL)

            break

        option_dict.get(option, lambda: print())()


    # -------------------------------------------------------------------------
    #                           INITIALIZE VARIABLES

    date_birth = df_option['Date of Birth'].values[0]
    b_state_code = df_option['Born State Code'].values[0]
    cl_state_code = df_option['Current Living State Code'].values[0]
    gender = df_option['Gender'].values[0]
    school_code = df_option['School Code'].values[0]
    user_provide_school = True if school_code is not None else False
    digits = digits_generator(gender = gender, start = digit_start, stop = digit_stop)

    if date_birth is None:
        list_date_birth = date_generator(
            start_date = start_date if start_date != '' else None,
            end_date = end_date if end_date != '' else None,
        )

    elif date_birth is not None:
        list_date_birth = [date_birth]

    if b_state_code is None:
        df_b_state_code = df['State Code'].drop_duplicates().reset_index(drop = True)

        if cl_state_code is not None:
            index = df_b_state_code.index[df_b_state_code == cl_state_code].tolist()[0] # Get index of cl_state_code in df_b_state_code
            df_b_state_code.iloc[index], df_b_state_code.iloc[0] = df_b_state_code.iloc[0], df_b_state_code.iloc[index] # Swap index of cl_state_code with index 0

        if school_code is not None:
            state_code = df.loc[df['School Code'] == school_code]['State Code'].values[0]
            index = df_b_state_code.index[df_b_state_code == state_code].tolist()[0]
            df_b_state_code.iloc[index], df_b_state_code.iloc[0] = df_b_state_code.iloc[0], df_b_state_code.iloc[index]

    elif b_state_code is not None:
        df_b_state_code = [b_state_code]

    if cl_state_code is None:

        if school_code is not None:
            df_cl_state_code = df.loc[df['School Code'] == school_code]['State Code'].values

        else:
            df_cl_state_code = df['State Code'].drop_duplicates().reset_index(drop = True)

            if b_state_code is not None:
                index = df_cl_state_code.index[df_cl_state_code == b_state_code].tolist()[0]
                df_cl_state_code.iloc[index], df_cl_state_code.iloc[0] = df_cl_state_code.iloc[0], df_cl_state_code.iloc[index]

    elif cl_state_code is not None:
        df_cl_state_code = [cl_state_code]


    # -------------------------------------------------------------------------
    #                           MAIN

    current_progress = 0
    for b_state_code in df_b_state_code:
        for date_birth in list_date_birth:
            for digit in digits:

                current_progress += 1
                total_progress = len(df_b_state_code) * len(list_date_birth) * len(digits)
                percentage_progress = str(round(current_progress / total_progress * 100, 3)) + '%'

                for cl_state_code in df_cl_state_code:

                    def print_basic():
                        cls()
                        print_state_or_school = str(Fore.RED + '\tGo Through Schools in State: ' + df.loc[df['State Code'] == cl_state_code]['State Name'].values[0] + '\n') if user_provide_school is False else str(Fore.RED + '\tGo Through School: ' + school_code + ' ' + df.loc[df['School Code'] == school_code]['School Name'].values[0] + '\n' + Style.RESET_ALL)
                        print(
                            tabulate(
                                df_valid_student,
                                ),
                            '',
                            Fore.RED + '\tNRIC State Code: ' + df.loc[df['State Code'] == b_state_code]['State Name'].values[0],
                            print_state_or_school
                        )

                    print_basic()

                    width_terminal = os.get_terminal_size().columns
                    spaces = width_terminal - len(percentage_progress) - 38 - 30
                    current_progress_line = '\t' + Back.BLACK + Fore.WHITE + ' (' + percentage_progress + ') ' + Back.YELLOW + Fore.BLACK + ' Current Progress: ' + Back.BLUE + Fore.BLACK + ' NRIC ' + date_birth + b_state_code + digit + ' ' * spaces + Style.RESET_ALL

                    print(
                        current_progress_line,
                        end = '\r'
                        )

                    response = nric_valid(
                        date_birth = date_birth,
                        state_code = b_state_code,
                        digit = digit
                        )

                    if response is False:
                        break

                    # Initiate School Code Variable
                    if user_provide_school is False:
                        df_school_code = df.loc[df['State Code'] == cl_state_code]['School Code']
                        length_school = str(len(df_school_code.values))

                    elif user_provide_school is not False:
                        df_school_code = [school_code]
                        length_school = '1'

                    print()
                    current_school_index = 0
                    for school_code in df_school_code:
                        current_school_index += 1
                        school_name = df.loc[df['School Code'] == school_code]['School Name'].values[0]
                        length_string = len(str(current_school_index) + length_school + school_code + school_name) + (5 if length_school != '1' else -2)
                        width_terminal = os.get_terminal_size().columns
                        spaces = width_terminal - length_string - 30

                        print(
                            '\t' + ((Back.BLACK + Fore.WHITE + ' (' + str(current_school_index) + '/' + length_school + ') ') if length_school != '1' else '') + Back.YELLOW + Fore.BLACK + ' ' + school_code + ' ' + Back.BLUE + Fore.BLACK + ' ' + school_name + ' ' * spaces + Style.RESET_ALL,
                            end = '\r'
                            )

                        response = nric_valid(
                            date_birth = date_birth,
                            state_code = b_state_code,
                            digit = digit,
                            school_code = school_code
                            )

                        if response is False:
                            continue

                        response = retrieve_details(
                            date_birth = date_birth,
                            state_code = b_state_code,
                            digit = digit,
                            school_code = school_code
                            )

                        df_response = pd.DataFrame(response)
                        df_valid_student = pd.concat(
                            [df_valid_student, df_response],
                            ignore_index = True
                            ).drop_duplicates()
                        DF().push_csv(
                            dataframe = df_valid_student,
                            file_name = 'Student_Details.csv'
                            )

                        print_basic()
                        print(
                            current_progress_line,
                        )

                        continue


def main():

    df = DF().pull_csv(
        ignore_validation = True,
        from_url = True
        )

    parser = argparse.ArgumentParser(
        description = 'Retrieve Student Details from any given details',
        epilog = textwrap.dedent(
            '''
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

            '''
            ),
        formatter_class = argparse.RawDescriptionHelpFormatter
        )

    parser.add_argument(
        '-v',
        '--version',
        action = 'version',
        version = '%(prog)s {0}'.format(get_version())
        )
    parser.add_argument(
        '-w',
        '--where',
        help = 'Show where is the data stored',
        action = 'store_true',
        default = False
    )
    parser.add_argument(
        '--print-flush',
        help = 'Whether to forcibly flush the stream',
        action = 'store_true',
        default = False
        )
    parser.add_argument(
        '--instant-start',
        help = 'Skip the menu and start immediately',
        action = 'store_true',
        default = False
        )
    parser.add_argument(
        '--tabulate-format',
        help = 'The format to use for tabulating the data',
        metavar = 'FORMAT',
        type = str,
        choices = ['plain', 'simple', 'github', 'grid', 'fancy_grid', 'pipe', 'orgtbl', 'jira', 'presto', 'pretty', 'psql', 'rst', 'mediawiki', 'moinmoin', 'youtrack', 'html', 'unsafehtml', 'latex', 'latex_raw', 'latex_booktabs', 'latex_longtable', 'textile', 'tsv'],
        default = 'psql'
        )
    parser.add_argument(
        '--database-validate-days',
        help = 'How many days can a DataBase.csv be valid, If 7, it will get update if exceeds 7 days count from the last update',
        metavar = 'DAYS',
        type = int,
        default = 7
        )
    parser.add_argument(
        '--digit-start',
        help = 'Generate NRIC last 4 digits start from this number',
        metavar = 'INTEGER',
        type = int,
        choices = range(0, 10000),
        default = 0
    )
    parser.add_argument(
        '--digit-stop',
        help = 'Generate NRIC last 4 digits stop at this number',
        metavar = 'INTEGER',
        type = int,
        choices = range(0, 10000),
        default = 10000
    )
    parser.add_argument(
        '--cl-state-code',
        help = 'State Code of the State where the student is living currently',
        metavar = 'CODE',
        type = str,
        choices = [x for x in df['State Code'].values],
    )
    parser.add_argument(
        '--b-state-code',
        help = 'State Code of the State where the student is born',
        metavar = 'CODE',
        type = str,
        choices = [x for x in df['State Code'].values],
    )
    parser.add_argument(
        '--school-code',
        help = 'School Code of the School',
        metavar = 'CODE',
        type = str.upper,
        choices = [x for x in df['School Code'].values],
    )
    parser.add_argument(
        '--birth-date',
        help = 'Birth Date of the Student',
        metavar = 'YYMMDD',
        type = lambda x: valid_date(x, is_argparse = True),
    )
    parser.add_argument(
        '--birth-date-start',
        help = 'Start date of a looping birth date',
        metavar = 'YYMMDD',
        type = lambda x: valid_date(x, is_argparse = True),
    )
    parser.add_argument(
        '--birth-date-end',
        help = 'End date of a looping birth date',
        metavar = 'YYMMDD',
        type = lambda x: valid_date(x, is_argparse = True),
    )
    parser.add_argument(
        '--gender',
        help = 'Gender of the Student',
        metavar = 'GENDER',
        choices = ['MALE', 'FEMALE'],
        type = str.upper,
    )

    args = parser.parse_args()

    if args.where is True:
        PATH = Path().user_data_dir
        print(PATH)
        try:
            import subprocess # Only available on Windows system, this will open the folder in the explorer
            FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            subprocess.run([FILEBROWSER_PATH, PATH])
        except:
            pass
        finally:
            sys.exit(0)


    try:
        _main(
            print_flush = args.print_flush,
            tabulate_format = args.tabulate_format,
            database_validate_days = args.database_validate_days,
            instant_start = args.instant_start,
            digit_start = args.digit_start,
            digit_stop = args.digit_stop,
            b_state_code = args.b_state_code,
            cl_state_code = args.cl_state_code,
            school_code = args.school_code,
            birth_date = args.birth_date,
            birth_date_start = args.birth_date_start,
            birth_date_end = args.birth_date_end,
            gender = args.gender,
        )

        cls()
        print(tabulate(df_valid_student), end = '\n\n')

    except KeyboardInterrupt:
        cls()
        try: print(tabulate(df_valid_student), end = '\n\n')
        except: pass
        print('\n\tInterrupted by user')

    except Exception:
        cls()
        try: print(tabulate(df_valid_student), end = '\n\n')
        except: pass
        print(traceback.format_exc())

    finally:
        print(
            '\tVersion: ' + get_version(),
            '\n\tThank you for using this program',
            '\tIf you wonder where the data is stored, here it is:',
            '\t' + Path().user_data_dir,
            '\n\tIf you have any issues or suggestions, please visit:',
            '\thttps://github.com/LynBean/My-Stalker',
            sep = '\n'
            )

        input('\n\t>ENTER<\n\t' + Style.RESET_ALL)
