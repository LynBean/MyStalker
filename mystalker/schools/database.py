
import os
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Callable
from typing import Optional

import pandas as pd
import requests

from ..constants import *
from ..utils import get_data_dir
from .district import pull_latest_district_data
from .school import pull_latest_school_data
from .state import pull_latest_state_data

# Initialize the data directory.
file_path: Path = get_data_dir().joinpath(SCHOOLS_FILENAME)

if not file_path.exists() or file_path.stat().st_size == 0:
    # To be faster, we will just pull the generated database file from the web instead.
    response = requests.get(DATABASE_FILE_URL)

    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(response.text)

    # Set the file's last modified time to the old date so that we can pull the latest database in the next run.
    os.utime(file_path, (27000, 27000))


def get_data(
    *,
    dtype: type=str,
    renew_interval: int=DEFAULT_DATABASE_RENEW_INTERVAL,
    skip_renew: bool=False,
    error_handler: Optional[Callable[[Exception], None]] = lambda e: None
) -> pd.DataFrame | pd.Series:
    """Retrieve data from the database.
    Get the latest data from the web if the database is older than the renew interval.
    """
    df: pd.DataFrame

    # Renew the database.csv file if it is older than the renew interval.
    if (
        datetime.utcfromtimestamp(os.path.getmtime(file_path)) < datetime.utcnow() - timedelta(days=renew_interval)
        and not skip_renew
    ):
        df = pull_latest_database(network_error_handler=error_handler)
        push_csv(df)
    else:
        df = pd.read_csv(file_path, dtype=dtype)

    return df

def push_csv(data: pd.DataFrame) -> None:
    """Push the latest data to the database
    """
    data = data.sort_values(by=["State Code", "District Code", "School Code"])
    data.to_csv(file_path, index=False, mode="w+", encoding="utf-8")


def pull_latest_database(
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> pd.DataFrame | pd.Series:
    """Update the database with latest data.
    """
    df = pd.DataFrame()
    states: Tuple[int, str] = pull_latest_state_data(network_error_handler=network_error_handler)

    for state_code_int in states[0]:
        state_code = str(state_code_int)
        districts: Tuple[str, str] = pull_latest_district_data(state_code, network_error_handler=network_error_handler)

        for district_code in districts[0]:
            schools: Tuple[str, str] = pull_latest_school_data(state_code, district_code, network_error_handler=network_error_handler)

            for i in range(len(schools[0])):
                df_temp = pd.DataFrame(
                    {
                        "State Code": [state_code],
                        "State Name": [states[1][states[0].index(state_code)]],
                        "District Code": [district_code],
                        "District Name": [districts[1][districts[0].index(district_code)]],
                        "School Code": [schools[0][i]],
                        "School Name": [schools[1][schools[0].index(schools[0][i])]],
                    }
                )

                df = pd.concat([df, df_temp])

    return df
