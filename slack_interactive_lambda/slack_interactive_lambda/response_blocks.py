from dataclasses import dataclass, field
from typing import List

from slack_sdk.models.blocks import Block


@dataclass
class ResponseBlocks:
    channel: str
    title: str
    blocks: List[Block] = field(default_factory=list)

    def add_block(self, block: Block):
        self.blocks.append(block)

    def to_message(self):
        return list(b.to_dict() for b in self.blocks)
