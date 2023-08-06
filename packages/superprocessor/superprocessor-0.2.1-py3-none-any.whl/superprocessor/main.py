
import subprocess as sp
from typing import (
    Union, Tuple
)

from superprocessor.util import (
    set_logs, set_defaults, log,
)


"""
Samo c 2021
Author: Samoto
"""


def cmd(* args: str, ** kwargs) -> Tuple[str, Union[str, None], int]:
    """
    :param args: list of strings --
        to be concatenated into stmt
    :return: tuple --
        of length 2: std (output, error)
    """

    set_defaults()

    if not args:
        log(f'leaving early: args = {args}')
        return tuple()

    for k, v in kwargs.items():
        {
            'log': lambda: set_logs(enabled=True),
        }.get(k, lambda: None)()

    stmt: [str] = []
    for arg in args:
        if ' ' in arg and isinstance(arg, str):
            stmt.extend(arg.split())
        else:
            stmt.append(str(arg))

    log(f'stmt built: {stmt}')

    resp = sp.run(stmt,
                  capture_output=True,
                  text=True)

    log(f'response: {resp}')

    return (
        resp.stdout,
        resp.stderr or None,
        resp.returncode,
    )
