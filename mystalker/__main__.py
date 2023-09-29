
import argparse
import time
from argparse import ArgumentTypeError
from datetime import datetime
from datetime import timedelta
from random import randint
from typing import Callable
from typing import Literal
from typing import Optional
from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from .checkpoint import Checkpoint
from .constants import *
from .schools import get_data
from .sessions import get_session
from .students import Student
from .students import append_student
from .ui.window import Window
from .utils import get_data_dir

school_df: pd.DataFrame


def digits_generator(
    *,
    gender: Literal[0, 1, 2]=None,
    start: Union[str, int]=0,
    stop: Union[str, int]=10000
) -> List[str]:
    """Generate a list of 4-digit numbers.

    Args:
        gender (int, optional):
            0 - Non binary, 1 - Male, 2 - Female.
            Male will be having Odd digit for the last digit,
            Female will be having Even digit for the last digit.

        start (int, optional): Starting range. Defaults to 0.
        stop (int, optional): Stopping range. Defaults to 10000.
    """
    # Validate parameters
    start: int = int(start)
    stop: int = int(stop)
    digits: str = []
    start = 0 if start <= 0 else 10000 if start >= 10000 else start
    stop = 10000 if stop >= 10000 else 0 if stop <= 0 else stop

    if start > stop:
        raise ValueError("Start cannot be greater than Stop")

    if gender == 1:
        start = start + 1 if start % 2 == 0 else start
    if gender == 2:
        start = start + 1 if start % 2 == 1 else start

    for x in range(start, stop, 1 if gender == 0 else 2):
        digits.append(str(x).zfill(4))

    return digits

def date_validate(date: str) -> str:
    """Validate date format.

    Args:
        date (str): Date in YYMMDD format.

    Raises:
        ValueError: If date is not in YYMMDD format.

    Returns:
        str: Date in YYMMDD format.
    """
    try:
        datetime.strptime(date, "%y%m%d")
        return date
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def date_generator(
    *,
    start: str="000101",
    stop: str=datetime.now()
) -> List[str]:
    """Generate a list of dates.

    Args:
        start (str, optional): Defaults to "000101".
        stop (str, optional): Defaults to datetime.now().
    """
    start_date: datetime = datetime.strptime(start, "%y%m%d")
    stop_date: datetime = datetime.strptime(stop, "%y%m%d")
    df_date: pd.DatetimeIndex = pd.date_range(
        start_date,
        stop_date - timedelta(days=1),
        freq="d"
    )
    dates: List[str] = [
        pd.to_datetime(date).strftime("%y%m%d")
        for date in df_date.values
    ]
    return dates

def is_student_exist(
    *,
    nric: str,
    school_code: Optional[str]=None,
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> bool:
    """Check if student exist.
    """
    session: requests.Session = get_session()
    url: str = f"{PAPAR_CARIAN_URL}?nokp={nric}"
    while True:
        try:
            response = session.get(
                url,
                timeout=5,
                verify=False
            )
            if not response.ok:
                continue
            if "Tidak Wujud" in response.text:
                return False
            if not url.startswith(PAPAR_CARIAN_PELAJAR_URL) and school_code is not None:
                url = f"{PAPAR_CARIAN_PELAJAR_URL}?nokp={nric}&kodsek={school_code}"
                continue
            break

        except NETWORK_ERROR_EXCEPTIONS as e:
            network_error_handler(e)
            time.sleep(randint(1, 5))
            continue
    return True

def retrieve_student(
    *,
    nric: str,
    school_code: str,
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> Optional[Student]:
    """Retrieve student information if exist.
    Else return None.
    """
    session: requests.Session = get_session()
    response: requests.Response

    # Verify student availability
    if not is_student_exist(
        nric=nric,
        school_code=school_code,
        network_error_handler=network_error_handler
    ):
        return None

    # Retrieve student information
    while True:
        try:
            response = session.get(
                IBUBAPA_SEMAK_URL,
                timeout=5,
                verify=False
            )
            if response.ok:
                break

        except NETWORK_ERROR_EXCEPTIONS as e:
            network_error_handler(e)
            time.sleep(randint(1, 5))
            continue

    soup = bs(response.text, "lxml")
    student_name = soup.find(lambda tag: tag.text.strip() == "NAMA MURID") \
        .find_next("td") \
        .find_next("td") \
        .text \
        .strip()

    df = school_df.loc[school_df["School Code"] == school_code]
    school_name = df["School Name"].values[0]
    state_code = df["State Code"].values[0]
    state_name = df["State Name"].values[0].split(" - ")[1]
    district_code = df["District Code"].values[0]
    district_name = df["District Name"].values[0].split(" - ")[1]

    return Student(
        state_code=state_code,
        state_name=state_name,
        district_code=district_code,
        district_name=district_name,
        school_code=school_code,
        school_name=school_name,
        student_name=student_name,
        student_nric=nric
    )

def _main(
    checkpoint: Checkpoint,
    database_renew_interval: int,
    ui: Window
) -> None:
    """Main function.
    """
    ui.append_log("Retrieving latest school information.")
    # Retrieve school information
    global school_df
    school_df = get_data(
        renew_interval=database_renew_interval,
        error_handler=lambda e: ui.set_error(e)
    )
    ui.append_log("School information retrieved.")

    # ---------------------------------------------------------------------------------------------
    #                                VALIDATE VARIABLES

    if checkpoint.birth_state_code is not None:
        if school_df.loc[school_df["State Code"] == checkpoint.birth_state_code].empty:
            raise ArgumentTypeError(f"State Code {checkpoint.birth_state_code} is not valid.")

    if checkpoint.current_living_state_code is not None:
        if school_df.loc[school_df["State Code"] == checkpoint.current_living_state_code].empty:
            raise ArgumentTypeError(f"State Code {checkpoint.current_living_state_code} is not valid.")

    if checkpoint.district_code is not None:
        if school_df.loc[school_df["District Code"] == checkpoint.district_code].empty:
            raise ArgumentTypeError(f"District Code {checkpoint.district_code} is not valid.")

    if checkpoint.school_code is not None:
        if school_df.loc[school_df["School Code"] == checkpoint.school_code].empty:
            raise ArgumentTypeError(f"School Code {checkpoint.school_code} is not valid.")

    # ---------------------------------------------------------------------------------------------
    #                                INITIALIZE VARIABLES

    ui.append_log("Initializing variables.")
    digits: List[str] = digits_generator(
        gender=checkpoint.gender,
        start=checkpoint.loop_digit_start,
        stop=checkpoint.loop_digit_stop
    )

    birth_dates: List[str]
    birth_state_df: pd.DataFrame
    current_living_state_df: pd.DataFrame

    if checkpoint.birth_date is None:
        birth_dates = date_generator(
            start=checkpoint.loop_birth_date_start,
            stop=checkpoint.loop_birth_date_stop
        )
    else:
        birth_dates = [checkpoint.birth_date]

    # As the user didn't specify the birth state code, we will max out the
    # chances of finding the student by prioritizing the state where the
    # student is currently living and the state where the school is located.
    # Priority: School State > District State > Current Living State
    if checkpoint.birth_state_code is None:
        # Head index of prioritized state code
        head_index: int = 0

        birth_state_df = school_df[["State Code", "State Name"]] \
            .drop_duplicates() \
            .reset_index(drop=True)

        # Prioritize the state where the school is located
        if checkpoint.school_code is not None:
            state_code: str = school_df.loc[
                school_df["School Code"] == checkpoint.school_code
            ] \
                ["State Code"] \
                .values[0]

            index: int = birth_state_df.index[
                birth_state_df["State Code"] == state_code
            ] \
                .tolist()[0]

            # Prevent pulling the last prioritized state code down
            birth_state_df.iloc[index], birth_state_df.iloc[head_index] = \
                birth_state_df.iloc[head_index].copy(), birth_state_df.iloc[index].copy()

            head_index += 1

        # Prioritize the state where the district is located
        if checkpoint.district_code is not None:
            state_code: str = school_df.loc[
                school_df["District Code"] == checkpoint.district_code
            ] \
                ["State Code"] \
                .values[0]

            index: int = birth_state_df.index[
                birth_state_df["State Code"] == state_code
            ] \
                .tolist()[0]

            birth_state_df.iloc[index], birth_state_df.iloc[head_index] = \
                birth_state_df.iloc[head_index].copy(), birth_state_df.iloc[index].copy()

            head_index += 1

        # Prioritize the state where the student is currently living
        if checkpoint.current_living_state_code is not None:
            # Get the index of the current living state code in birth state code dataframe
            index: int = birth_state_df.index[
                birth_state_df["State Code"] == checkpoint.current_living_state_code
            ] \
                .tolist()[0]

            # Move the current living state code to the top of the dataframe
            birth_state_df.iloc[index], birth_state_df.iloc[head_index] = \
                birth_state_df.iloc[head_index].copy(), birth_state_df.iloc[index].copy()


    # If the user specified the birth state code, we will only search for students in that state.
    else:
        birth_state_df = school_df.loc[school_df["State Code"] == checkpoint.birth_state_code] \
            [["State Code", "State Name"]] \
            .drop_duplicates() \
            .reset_index(drop=True)


    # If the user specified the school code, or the district code,
    # then we will only loop the schools in that state.
    if checkpoint.school_code is not None or checkpoint.district_code is not None:
        if checkpoint.school_code is not None:
            current_living_state_df = school_df.loc[school_df["School Code"] == checkpoint.school_code]

        elif checkpoint.district_code is not None:
            current_living_state_df = school_df.loc[school_df["District Code"] == checkpoint.district_code]


    # Else we will max out the chances of finding the student by prioritizing the state
    elif checkpoint.current_living_state_code is None:
        if checkpoint.birth_state_code is not None:
            current_living_state_df = school_df.loc[school_df["State Code"] == checkpoint.birth_state_code] \
                .drop_duplicates() \
                .reset_index(drop=True)

            index: int = current_living_state_df.index[
                current_living_state_df["State Code"] == checkpoint.birth_state_code
            ] \
                .tolist()[0]

            current_living_state_df.iloc[index], current_living_state_df.iloc[head_index] = \
                current_living_state_df.iloc[head_index].copy(), current_living_state_df.iloc[index].copy()


        # Otherwise, we will just use the same settings as the birth states
        else:
            current_living_state_df = birth_state_df.copy()

    # If the user specified the current living state code, then we will only loop the schools in that state.
    else:
        current_living_state_df = school_df.loc[school_df["State Code"] == checkpoint.current_living_state_code]


    current_living_state_df = current_living_state_df \
        [["State Code", "State Name"]] \
        .drop_duplicates() \
        .reset_index(drop=True)



    # ---------------------------------------------------------------------------------------------
    #                                START SCRAPING


    current_progress: int = 0
    total_progress: int = len(birth_state_df) * len(birth_dates) * len(digits)


    for birth_state_code, birth_state_name in birth_state_df.values:
        for date in birth_dates:
            for digit in digits:

                current_progress += 1
                progress_percentage: float = round(current_progress / total_progress * 100, 4)
                ui.set_progression(progress_percentage)

                # ---------------------------------------------------------------------------------
                #                    CHECKPOINT RESUMING MECHANISM

                if not checkpoint.is_resumed():
                    ui.set_info("Running checkpoint resuming mechanism.")
                    # Indicate first run
                    if (
                        checkpoint.current_loop_birth_state_code == None
                        and checkpoint.current_loop_birth_date == None
                        and checkpoint.current_loop_digit == None
                    ):
                        checkpoint.resumed = True
                        ui.append_log("Checkpoint resumed.")

                    # Not the first run, so keep skipping until we reach the last checkpoint
                    elif (
                        checkpoint.current_loop_birth_state_code != birth_state_code
                        or checkpoint.current_loop_birth_date != date
                        or checkpoint.current_loop_digit != digit
                    ):
                        continue

                    elif (
                        checkpoint.current_loop_school_code == None
                        and checkpoint.current_loop_current_living_state_code == None
                    ):
                        checkpoint.resumed = True
                        ui.append_log("Checkpoint resumed.")

                if checkpoint.is_resumed():
                    checkpoint.current_loop_birth_state_code = birth_state_code
                    checkpoint.current_loop_birth_date = date
                    checkpoint.current_loop_digit = digit
                    checkpoint.current_loop_current_living_state_code = None
                    checkpoint.current_loop_school_code = None
                    checkpoint.save()


                # ---------------------------------------------------------------------------------
                #                  SCRAPE

                nric: str = f"{date}{birth_state_code}{digit}"
                ui.set_info(f"Birth Date: {date} | Birth State: {birth_state_name} | Digit: {digit}")

                response: bool = is_student_exist(nric=nric, network_error_handler=lambda x: ui.set_error(x))

                if not response:
                    continue

                ui.append_log(f"Student {nric} exists. Require school information in order to retrieve student information.")

                current_state_progress: int = 0
                total_state_progress: int = len(current_living_state_df)


                for living_state_code, living_state_name in current_living_state_df.values:
                    current_state_progress += 1

                    if checkpoint.school_code is not None:
                        district_df: pd.DataFrame = school_df.loc[school_df["School Code"] == checkpoint.school_code]

                    elif checkpoint.district_code is not None:
                        district_df: pd.DataFrame = school_df.loc[school_df["District Code"] == checkpoint.district_code]

                    else:
                        district_df: pd.DataFrame = school_df.loc[school_df["State Code"] == living_state_code]

                    district_df = district_df \
                        [["District Code", "District Name"]] \
                        .drop_duplicates() \
                        .reset_index(drop=True)


                    current_district_progress: int = 0
                    total_district_progress: int = len(district_df)

                    for district_code, district_name in district_df.values:
                        current_district_progress += 1

                        if checkpoint.school_code is None:
                            district_school_df: pd.DataFrame = school_df.loc[school_df["District Code"] == district_code]

                        else:
                            district_school_df: pd.DataFrame = school_df.loc[school_df["School Code"] == checkpoint.school_code]

                        district_school_df = district_school_df \
                            [["School Code", "School Name"]] \
                            .drop_duplicates() \
                            .reset_index(drop=True)

                        current_school_progress: int = 0
                        total_school_progress: int = len(district_school_df)

                        for school_code, school_name in district_school_df.values:
                            current_school_progress += 1

                            # -------------------------------------------------------------------------
                            #          CHECKPOINT RESUMING MECHANISM


                            if not checkpoint.is_resumed():
                                if checkpoint.current_loop_school_code != school_code:
                                    continue

                                checkpoint.resumed = True
                                ui.append_log("Checkpoint resumed.")

                            if checkpoint.is_resumed():
                                checkpoint.current_loop_current_living_state_code = living_state_code
                                checkpoint.current_loop_school_code = school_code
                                checkpoint.save()


                            # -------------------------------------------------------------------------
                            #          SCRAPE

                            ui.set_info(
                                f"NRIC: {nric} " + \
                                f"| ({current_state_progress}/{total_state_progress}) State: {living_state_name} " + \
                                f"| ({current_district_progress}/{total_district_progress}) District: {district_name} " + \
                                f"| ({current_school_progress}/{total_school_progress}) School: {school_code} {school_name}"
                            )

                            response: bool = is_student_exist(
                                nric=nric,
                                school_code=school_code,
                                network_error_handler=lambda x: ui.set_error(x)
                            )

                            if not response:
                                continue

                            ui.append_log(f"Student {nric} found. Retrieving student information")

                            student: Student = retrieve_student(
                                nric=nric,
                                school_code=school_code,
                                network_error_handler=lambda x: ui.set_error(x)
                            )

                            if student is None:
                                ui.append_log(f"Student {nric} not found in {school_code} {school_name}. This should not happen.")
                                continue

                            append_student(student) # Append student to database
                            ui.append_student(student) # Append student to UI


def main():
    from . import __version__

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"mystalker {__version__}"
    )
    parser.add_argument(
        "-w",
        "--where",
        help="Specify the directory to store the database.",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--database-renew-interval",
        help="Specify the database renew interval in days.",
        metavar="DAYS",
        type=int,
        default=DEFAULT_DATABASE_RENEW_INTERVAL
    )

    def valid_digit(value: str) -> str:
        if int(value) not in range(0, 10000):
            raise ArgumentTypeError(f"{value} must be in range 0-9999")
        return value.zfill(4)

    parser.add_argument(
        "--loop-digit-start",
        help="Specify the starting range for digits.",
        metavar="DIGIT",
        type=valid_digit,
        default=DEFAULT_LOOP_DIGIT_START
    )
    parser.add_argument(
        "--loop-digit-stop",
        help="Specify the stopping range for digits.",
        metavar="DIGIT",
        type=valid_digit,
        default=DEFAULT_LOOP_DIGIT_STOP
    )
    parser.add_argument(
        "--birth-state-code",
        help="Specify the state where the student was born.",
        metavar="STATE_CODE",
        type=str.upper,
        default=None
    )
    parser.add_argument(
        "--current-living-state-code",
        help="Specify the state where the student is currently living.",
        metavar="STATE_CODE",
        type=str.upper,
        default=None
    )
    parser.add_argument(
        "--district-code",
        help="Specify the district where the student is currently living.",
        metavar="DISTRICT_CODE",
        type=str.upper,
        default=None
    )
    parser.add_argument(
        "--school-code",
        help="Specify the school code.",
        metavar="SCHOOL_CODE",
        type=str.upper,
        default=None
    )
    parser.add_argument(
        "--birth-date",
        help="Specify the student's birth date in YYMMDD format.",
        metavar="YYMMDD",
        type=date_validate,
        default=None
    )
    parser.add_argument(
        "--loop-birth-date-start",
        help="Specify the starting range for birth date.",
        metavar="YYMMDD",
        type=date_validate,
        default=DEFAULT_LOOP_BIRTH_DATE_START
    )
    parser.add_argument(
        "--loop-birth-date-stop",
        help="Specify the stopping range for birth date.",
        metavar="YYMMDD",
        type=date_validate,
        default=DEFAULT_LOOP_BIRTH_DATE_STOP
    )
    parser.add_argument(
        "--gender",
        help="Specify the gender of the student.",
        metavar="GENDER",
        type=str.lower,
        choices=["male", "female", "none-binary"],
        default="none-binary"
    )
    parser.add_argument(
        "-c",
        "--checkpoint",
        help="Enable checkpoint resuming mechanism.",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "-f",
        "--checkpoint-file",
        help="Specify the checkpoint filepath.",
        metavar="FILEPATH",
        type=str,
        default=None
    )
    parser.add_argument(
        "--nogui",
        help="Disable GUI.",
        action="store_true",
        default=False
    )

    args: argparse.Namespace = parser.parse_args()

    if args.where:
        print(get_data_dir())
        return

    gender: Literal[0, 1, 2] = 1 if args.gender == "male" \
        else 2 if args.gender == "female" \
        else 0

    cp: Checkpoint
    cp_args: dict = {
        "loop_digit_start": args.loop_digit_start,
        "loop_digit_stop": args.loop_digit_stop,
        "school_code": args.school_code,
        "birth_state_code": args.birth_state_code,
        "current_living_state_code": args.current_living_state_code,
        "district_code": args.district_code,
        "birth_date": args.birth_date,
        "loop_birth_date_start": args.loop_birth_date_start,
        "loop_birth_date_stop": args.loop_birth_date_stop,
        "gender": gender
    }

    if args.checkpoint_file is not None:
        cp = Checkpoint(args.checkpoint_file, **cp_args)
    elif args.checkpoint:
        cp = Checkpoint(CHECKPOINT_FILENAME, **cp_args)
    else:
        cp = Checkpoint(**cp_args)

    with Window(nogui=args.nogui) as ui:
        ui.set_header(
            f"MyStalker {__version__} | Press 'W' or 'S' to scroll up & down\n" + \
            f"Save directory: \"{get_data_dir().joinpath(STUDENTS_FILENAME)}\""
        )
        _main(
            checkpoint=cp,
            database_renew_interval=args.database_renew_interval,
            ui=ui
        )
