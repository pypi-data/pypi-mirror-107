from datetime import datetime
from enum import Enum, unique
from typing import Union


@unique
class Index(Enum):
    HEADER = 1
    BEGIN = 2
    END = 3


def int_index_to_str(idx: int) -> str:
    if not (isinstance(idx, int) and not isinstance(idx, bool)):
        raise TypeError
    return f'int{idx}'


def str_to_int_index(idx_str: str) -> int:
    if not isinstance(idx_str, str):
        raise TypeError
    assert idx_str.startswith('int')
    int_str = idx_str.replace('int', '')
    assert int_str.lstrip('-').isnumeric()
    return int(int_str)


def datetime_index_to_str(dt: datetime) -> str:
    if not isinstance(dt, datetime):
        raise TypeError
    return f'ts{dt.timestamp()}'


def str_to_datetime_index(idx_str: str) -> datetime:
    if not isinstance(idx_str, str):
        raise TypeError
    assert idx_str.startswith('ts')
    float_str = idx_str.replace('ts', '')
    assert float_str.replace('.', '').isnumeric(), f'{float_str} does not look like a float'
    return datetime.fromtimestamp(float(float_str))


def index_to_str(index: Union[int, datetime, Index]) -> str:
    if isinstance(index, int):
        index_str = int_index_to_str(index)
    elif isinstance(index, datetime):
        index_str = datetime_index_to_str(index)
    elif isinstance(index, Index):
        index_str = str(index.name)
    else:
        raise TypeError(f'Type of index {type(index)} not valid for Tracker.')
    return index_str


def str_to_index(index_str: str) -> Union[int, datetime, Index]:
    if index_str.startswith('int'):
        return str_to_int_index(index_str)
    if index_str.startswith('ts'):
        return str_to_datetime_index(index_str)
    for ind in Index:
        if index_str == ind.name:
            return ind
    raise ValueError(f'Could not parse index {index_str}')
