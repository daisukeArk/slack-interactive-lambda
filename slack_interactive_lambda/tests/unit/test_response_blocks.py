from slack_interactive_lambda.response_blocks import ResponseBlocks


class TestResponseBlocks:
    def test_initialize(self):
        target = ResponseBlocks(
            channel="channel_name",
            title="title",
        )

        assert target.channel == "channel_name"
        assert target.title == "title"
        assert target.blocks == []
