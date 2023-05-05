from urllib.parse import parse_qs

from .slack_interactive_route import SlackInteractiveRoute
from .slack_interactive_router import SlackInteractiveRouter


class SlackSlashCommand:
    def __init__(self, event: dict, router: SlackInteractiveRouter) -> None:
        self._router = router
        self._target_route: SlackInteractiveRoute = None

        self._event = event
        self._params = parse_qs(event["body"])

    @property
    def is_invoked(self) -> str:
        return self._event.get("is_invoked", False)

    @property
    def team_id(self) -> str:
        return self._params.get("team_id")[0]

    @property
    def team_domain(self) -> str:
        return self._params.get("team_domain")[0]

    @property
    def channel_id(self) -> str:
        return self._params.get("channel_id")[0]

    @property
    def channel_name(self) -> str:
        return self._params.get("channel_name")[0]

    @property
    def user_id(self) -> str:
        return self._params.get("user_id")[0]

    @property
    def user_name(self) -> str:
        return self._params.get("user_name")[0]

    @property
    def api_app_id(self) -> str:
        return self._params.get("api_app_id")[0]

    @property
    def is_enterprise_install(self) -> str:
        return self._params.get("is_enterprise_install")[0]

    @property
    def response_url(self) -> str:
        return self._params.get("response_url")[0]

    @property
    def trigger_id(self) -> str:
        return self._params.get("trigger_id")[0]

    @property
    def command(self) -> str:
        return self._params.get("command")[0]

    @property
    def command_text(self) -> str:
        return self._params.get("text")[0]

    @property
    def command_full_text(self) -> str:
        return " ".join([self.command, self.command_text])

    @property
    def command_text_without_slash_command(self) -> str:
        return " ".join([word.lower() for word in self.command_full_text.split()[1:]])

    @property
    def slash_command_without_slash_string(self) -> str:
        return self.command_full_text.split()[0].lower()[1:]

    @property
    def verb(self) -> str:
        return self.route.verb if self.route is not None else ""

    @property
    def command_text_args(self):
        if self.route is None:
            raise Exception("Not Exists Command")

        verb_word_count = 0 if self.route.verb == "*" else len(self.route.verb.split())
        return self.command_full_text.split()[verb_word_count + 1 :]

    def _get_route(self):
        def sort_command_text_word_count(router: SlackInteractiveRoute):
            return 0 if router.verb == "*" else len(router.verb.split())

        _target_route = None

        for route in sorted(self._router.routers, key=sort_command_text_word_count, reverse=True):
            if route.allow_command not in [self.slash_command_without_slash_string, "*"]:
                continue

            if self.command_text_without_slash_command.startswith(route.verb) or route.verb == "*":
                _target_route = route
                break

        return _target_route

    @property
    def route(self) -> SlackInteractiveRoute:
        if self._target_route is not None:
            return self._target_route

        self._target_route = self._get_route()

        return self._target_route
