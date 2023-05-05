from slack_interactive_lambda.slack_interactive_route import SlackInteractiveRoute
from slack_interactive_lambda.slack_interactive_router import SlackInteractiveRouter
from slack_interactive_lambda.slack_slash_command import SlackSlashCommand


class TestSlackSlashCommand:
    def test_initialize(self):
        body_strings = [
            "team_id=T12345678",
            "team_domain=example-team",
            "channel_id=C1234567890",
            "channel_name=pj-example",
            "user_id=U1234567890",
            "user_name=example_user",
            "api_app_id=xxxxx",
            "is_enterprise_install=false",
            "response_url=x",
            "trigger_id=x",
            "command=%2Fworkflow",
            "text=ec2%20list%20running",
        ]

        mock_req = {
            "body": "&".join(body_strings),
        }

        router = SlackInteractiveRouter()
        router.register(
            SlackInteractiveRoute(
                verb="ec2 list",
                handler=lambda x: x + 1,
            )
        )

        target = SlackSlashCommand(mock_req, router)

        assert target.verb == "ec2 list"
        assert target.team_id == "T12345678"
        assert target.team_domain == "example-team"
        assert target.channel_id == "C1234567890"
        assert target.channel_name == "pj-example"
        assert target.user_id == "U1234567890"
        assert target.user_name == "example_user"
        assert target.api_app_id == "xxxxx"
        assert target.response_url == "x"
        assert target.command == "/workflow"
        assert target.command_text == "ec2 list running"
        assert target.command_full_text == "/workflow ec2 list running"
        assert target.command_text_without_slash_command == "ec2 list running"
        assert target.slash_command_without_slash_string == "workflow"
        assert target.command_text_args == ["running"]
