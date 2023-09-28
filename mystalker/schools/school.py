
import time
from random import randint
from typing import Callable
from typing import Optional
from typing import Tuple

import requests
from bs4 import BeautifulSoup as bs

from ..constants import *
from ..sessions import get_session


def pull_latest_school_data(
    state_code: str,
    district_code: str,
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> Tuple[str, str]:
    """Pull latest data from the web.
    """
    session: requests.Session = get_session()

    while True:
        try:
            response = session.get(
                f"{SENARAI_SEKOLAH_URL}?kodnegeri={state_code}&kodppd={district_code}",
                verify = False,
                timeout = 5
            )
            if response.ok:
                break
        except NETWORK_ERROR_EXCEPTIONS as e:
            network_error_handler(e)
            time.sleep(randint(1, 5))
            continue

    soup = bs(response.text, "lxml")

    schools = ([], [])
    for value in soup.find_all("option") :

        if value["value"] != "" :
            schools[0].append(value["value"])
        if value.text not in ("-PILIH SEKOLAH-") :
            schools[1].append(value.text)

    return schools
