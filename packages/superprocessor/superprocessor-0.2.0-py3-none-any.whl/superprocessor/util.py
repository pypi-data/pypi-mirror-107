
import os


"""
Samo c 2021
Author: Samoto
"""

LOGS_ENABLED = False


def set_logs(enabled: bool = False) -> None:
    """
    :param enabled: prioritized means of accepting log enablement
        backup - environment var \"SUPER_LOGS\" set to \"TRUE\"
    :return: None
    """
    global LOGS_ENABLED
    LOGS_ENABLED = enabled or os.environ.get('SUPER_LOGS', '').lower() == 'true'


def set_defaults() -> None:
    """
    sets default configurations
    :param: None
    :return: None
    """
    set_logs(enabled=False)


def log(msg: str) -> None:
    """
    :param msg: str to log
    :return: None
    """
    if not LOGS_ENABLED:
        return
    print('(SUPER) ', msg)
