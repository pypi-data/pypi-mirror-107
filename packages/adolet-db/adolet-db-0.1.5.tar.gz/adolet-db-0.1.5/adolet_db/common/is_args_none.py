from typing import List, Any


def is_args_none(args: List[Any]) -> None:
    '''Check if any of the argumements is None'''
    if not all(args):
        raise Exception("ERROR - Arguments can't be None")
