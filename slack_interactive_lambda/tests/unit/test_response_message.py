from slack_interactive_lambda.response_message import ResponseMessage


class TestResponseMessage:
    def test_initialize(self):
        target = ResponseMessage(
            channel="channel_name",
            text="text",
        )

        assert target.channel == "channel_name"
        assert target.text == "text"
