import json
from typing import Any, Dict, Literal

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.webhook import WebhookClient

from .exceptions import InvalidCommand, PermissionDenied
from .response_blocks import ResponseBlocks
from .response_file import ResponseFile
from .response_message import ResponseMessage
from .slack_interactive_route import SlackInteractiveRoute
from .slack_interactive_router import SlackInteractiveRouter
from .slack_slash_command import SlackSlashCommand


class SlackInteractive:
    def __init__(
        self,
        lambda_client,
        bot_token: str = None,
        signing_secret: str = None,
        response_type: Literal["in_channel", "ephemeral"] = "in_channel",
        allow_users: list[str] = [],
        allow_channels: list[str] = [],
    ) -> None:
        self._router = SlackInteractiveRouter()

        self._lambda_client = lambda_client
        self._bot_token = bot_token
        self._signing_secret = signing_secret
        self._response_type = response_type
        self._allow_users = allow_users
        self._allow_channels = allow_channels

    def set_signing_secret(self, value):
        self._signing_secret = value

    def set_bot_token(self, value):
        self._bot_token = value

    def route(
        self,
        verb,
        allow_users=[],
        allow_commands=["*"],
        is_disable_response_accept=False,
        is_disable_response_callback=False,
    ):
        def inner_func(f: callable):
            for allow_command in allow_commands:
                self._router.register(
                    SlackInteractiveRoute(
                        verb=verb.lower(),
                        handler=f,
                        allow_command=allow_command,
                        allow_users=allow_users,
                        is_disable_response_accept=is_disable_response_accept,
                        is_disable_response_callback=is_disable_response_callback,
                    )
                )
            return f

        return inner_func

    def execute(self, event: Dict[str, Any], context):
        if self._bot_token is None:
            raise Exception("Required Input")
        if self._signing_secret is None:
            raise Exception("Required Input")

        if not self._authenticate(event, context):
            return {
                "statusCode": 403,
                "body": json.dumps(
                    {
                        "response_type": self._response_type,
                        "text": "failed",
                    }
                ),
            }

        command = SlackSlashCommand(event, self._router)

        if self._allow_channels and (
            command.channel_id not in self._allow_channels and command.channel_name not in self._allow_channels
        ):
            raise PermissionDenied(f"{command.channel_id}: {command.channel_name}")
        if self._allow_users and (
            command.user_id not in self._allow_users and command.user_name not in self._allow_users
        ):
            raise PermissionDenied(f"{command.user_id}: {command.user_name}")

        if not command.route:
            raise InvalidCommand()
        if command.route.allow_users and (
            command.user_id not in command.route.allow_users and command.user_name not in command.route.allow_users
        ):
            raise PermissionDenied(f"{command.user_id}: {command.user_name}")

        if not command.is_invoked:
            payload = event | {"is_invoked": True}
            self._invoke_lambda(context.invoked_function_arn, json.dumps(payload).encode())

            return self._build_response(f"{command.verb} accepted.")

        response = self._call_handler(command)

        if not command.route.is_disable_response_callback:
            if type(response) == ResponseMessage:
                self._send_result_message(command, response)
            elif type(response) == ResponseFile:
                self._send_result_files(command, response)
            elif type(response) == ResponseBlocks:
                self._send_result_blocks(command, response)
            else:
                raise Exception("Not Exists Response")

        return None

    def _call_handler(self, command: SlackSlashCommand):
        if not command.route:
            raise InvalidCommand()

        return command.route.handler(command)

    def _send_result_message(self, command: SlackSlashCommand, res: ResponseMessage):
        webhook = WebhookClient(command.response_url)
        webhook.send(text=res.text, response_type=self._response_type)

    def _send_result_blocks(self, command: SlackSlashCommand, res: ResponseBlocks):
        webhook = WebhookClient(command.response_url)
        webhook.send(blocks=res.to_message(), response_type=self._response_type)

    def _send_result_files(self, command: SlackSlashCommand, res: ResponseFile):
        client = WebClient(token=self._bot_token)

        response = client.files_upload_v2(
            channel=res.channel,
            title=res.title,
            filename=res.filename,
            file=res.file,
            initial_comment=res.initial_comment,
            request_file_info=False,
        )

        response.validate()

    def _invoke_lambda(self, function_name: str, payload: bytes):
        self._lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="Event",
            # LogType='None'|'Tail',
            # ClientContext='string',
            Payload=payload,
            # Qualifier='string'
        )

    def _authenticate(self, event, context) -> bool:
        signature_verifier = SignatureVerifier(signing_secret=self._signing_secret)
        return signature_verifier.is_valid_request(body=event["body"], headers=event["headers"])

    def _build_response(self, message: str) -> dict:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "response_type": self._response_type,
                    "text": message,
                }
            ),
        }
