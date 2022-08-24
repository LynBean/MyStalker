
import requests
import time
import urllib3

from bs4 import BeautifulSoup as bs

from .constants import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class District(object):


    @staticmethod
    def pull_latest(
        state_code: str
        ) -> tuple:
        '''
        Pull latest data from the web.
        '''

        session = requests.Session()
        session.headers.update(
        USER_AGENTS
        )

        while True:
            try:
                html_response = session.get(
                    '{0}?kodnegeri={1}'.format(
                        SENARAI_PPD_URL,
                        state_code
                        ),
                    verify = False
                    )
                if html_response.status_code == 200:
                    break
            except NETWORK_ERROR_EXCEPTIONS:
                time.sleep(5)
                continue

        soup = bs(html_response.text, 'lxml')

        districts = ([], [])
        for value in soup.find_all('option') :

            if value['value'] != '' :
                districts[0].append(value['value'])
            if value.text not in ('-PILIH PPD-') :
                districts[1].append(value.text)

        return districts
