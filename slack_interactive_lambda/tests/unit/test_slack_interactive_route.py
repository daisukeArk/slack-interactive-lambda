from slack_interactive_lambda.slack_interactive_route import SlackInteractiveRoute


class TestSlackInteractiveRoute:
    def test_initialize(self):
        route = SlackInteractiveRoute(
            verb="help",
            handler=lambda x: x + 1,
        )

        assert route.verb == "help"
        assert route.handler(1) == 2
        assert route.allow_command == "*"
        assert route.allow_channels == []
        assert route.allow_users == []
        assert not route.is_disable_response_accept
        assert not route.is_disable_response_callback
