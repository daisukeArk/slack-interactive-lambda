import json

from slack_interactive_lambda.slack_interactive import SlackInteractive


class TestSlackInteractive:
    def test_initialize(self, mocker):
        lambda_client_mock = mocker.Mock()

        target = SlackInteractive(lambda_client_mock)

        @target.route(verb="ec2 list")
        def dummy_func(cmd):
            pass

        assert len(target._router.routers) == 1

    def test_set_signing_secret(self, mocker):
        lambda_client_mock = mocker.Mock()

        target = SlackInteractive(lambda_client_mock)
        target.set_signing_secret("x")

        assert target._signing_secret == "x"

    def test_set_bot_token(self, mocker):
        lambda_client_mock = mocker.Mock()

        target = SlackInteractive(lambda_client_mock)
        target.set_bot_token("x")

        assert target._bot_token == "x"

    def test_execute(self, lambda_context, mocker):
        lambda_client_mock = mocker.Mock()

        target = SlackInteractive(lambda_client_mock)
        target.set_bot_token("x")
        target.set_signing_secret("x")

        @target.route(verb="ec2 list")
        def dummy_func(cmd):
            return "test"

        mocker.patch.object(target, "_authenticate", return_value=True)

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

        response = target.execute(mock_req, lambda_context)

        assert response == {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "response_type": "in_channel",
                    "text": "ec2 list accepted.",
                }
            ),
        }
