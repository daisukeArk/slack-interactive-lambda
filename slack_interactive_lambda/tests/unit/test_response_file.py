from slack_interactive_lambda.response_file import ResponseFile


class TestResponseFile:
    def test_initialize(self):
        target = ResponseFile(
            channel="channel_name",
            title="title",
            filename="filename",
            initial_comment="initial_comment",
            file=b"hello",
        )

        assert target.channel == "channel_name"
        assert target.title == "title"
        assert target.filename == "filename"
        assert target.initial_comment == "initial_comment"
        assert target.file == b"hello"
