from dataclasses import dataclass
from typing import Union


@dataclass
class ResponseFile:
    channel: str
    title: str
    filename: str
    file: Union[str, bytes]
    initial_comment: str
