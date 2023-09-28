
import random
from typing import List

import requests

from .constants import USER_AGENT


def get_session() -> requests.Session:
    """Randomly renew a session.
    Return a random session from the sessions list.
    """
    sessions[random.randint(0, total_session - 1)] = _get_new_session()
    return random.choice(sessions)

def _get_new_session() -> requests.Session:
    """Get a requests session.
    """
    session = requests.Session()
    session.headers.update(USER_AGENT)
    return session


total_session: int = 20
sessions: List[requests.Session] = [
    _get_new_session()
    for _ in range(total_session)
]
