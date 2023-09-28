
import time
from random import randint
from typing import Callable
from typing import Optional

import requests
from bs4 import BeautifulSoup as bs

from ..constants import *
from ..sessions import get_session


def pull_latest_district_data(
    state_code: str,
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> Tuple[str, str]:
    """Pull latest data from the web.`
    """
    session: requests.Session = get_session()

    while True:
        try:
            response = session.get(
                f"{SENARAI_PPD_URL}?kodnegeri={state_code}",
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

    districts = ([], [])
    for value in soup.find_all("option") :

        if value["value"] != "" :
            districts[0].append(value["value"])
        if value.text not in ("-PILIH PPD-") :
            districts[1].append(value.text)

    return districts
