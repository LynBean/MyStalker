
import time
from random import randint
from typing import Callable
from typing import Optional

import requests
from bs4 import BeautifulSoup as bs

from ..constants import *
from ..sessions import get_session


def pull_latest_state_data(
    network_error_handler: Optional[Callable[[NETWORK_ERROR_EXCEPTIONS], None]] = lambda e: None
) -> Tuple[int, str]:
    """Pull latest data from the web.
    """
    session: requests.Session = get_session()

    while True:
        try:
            response = session.get(
                IBUBAPA_MAIN_URL,
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

    states = ([], [])
    for value in soup.find_all("option") :

        if value["value"] != "" :
            states[0].append(value["value"])
        if value.text not in ("-PILIH NEGERI-", "-PILIH DAERAH-", "-PILIH SEKOLAH-") :
            states[1].append(value.text)

    return states
