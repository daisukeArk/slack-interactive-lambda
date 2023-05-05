from dataclasses import dataclass, field


@dataclass
class SlackInteractiveRoute:
    verb: str
    handler: callable
    allow_command: str = "*"
    allow_channels: list[str] = field(default_factory=list)
    allow_users: list[str] = field(default_factory=list)
    is_disable_response_accept: bool = False
    is_disable_response_callback: bool = False
