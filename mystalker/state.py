
import time
import requests
import urllib3

from bs4 import BeautifulSoup as bs

from .constants import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class State:


    @staticmethod
    def pull_latest() -> tuple:
        """
        Pull latest data from the web.
        """

        session = requests.Session()

        while True:
            try:
                html_response = session.get(
                    IBUBAPA_MAIN_URL,
                    verify = False
                    )
                break
            except NETWORK_ERROR_EXCEPTIONS:
                time.sleep(5)
                continue

        soup = bs(html_response.text, 'lxml')

        states = ([], [])
        for value in soup.find_all('option') :

            if value['value'] != '' :
                states[0].append(value['value'])
            if value.text not in ('-PILIH NEGERI-', '-PILIH DAERAH-', '-PILIH SEKOLAH-') :
                states[1].append(value.text)

        return states
