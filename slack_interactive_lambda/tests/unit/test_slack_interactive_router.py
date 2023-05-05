from slack_interactive_lambda.slack_interactive_route import SlackInteractiveRoute
from slack_interactive_lambda.slack_interactive_router import SlackInteractiveRouter


class TestSlackInteractiveRouter:
    def test_initialize(self):
        router = SlackInteractiveRouter()

        assert router.routers == []

    def test_register(self):
        router = SlackInteractiveRouter()

        route1 = SlackInteractiveRoute(
            verb="help",
            handler=None,
        )
        route2 = SlackInteractiveRoute(
            verb="ask",
            handler=None,
        )

        router.register(route1)
        router.register(route2)

        assert len(router.routers) == 2
        assert router.routers[0].verb == "help"
        assert router.routers[1].verb == "ask"
