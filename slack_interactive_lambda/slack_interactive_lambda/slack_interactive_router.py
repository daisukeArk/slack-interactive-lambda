from dataclasses import dataclass, field

from .slack_interactive_route import SlackInteractiveRoute


@dataclass
class SlackInteractiveRouter:
    routers: list[SlackInteractiveRoute] = field(default_factory=list)

    def register(self, route: SlackInteractiveRoute):
        self.routers.append(route)
