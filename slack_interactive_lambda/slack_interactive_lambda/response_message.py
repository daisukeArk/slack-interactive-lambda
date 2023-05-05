from dataclasses import dataclass


@dataclass
class ResponseMessage:
    channel: str
    text: str
