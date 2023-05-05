import logging
from logging import NullHandler

from .slack_interactive import SlackInteractive

__author__ = "Daisuke Araki"
__version__ = "0.1.0"

__all__ = ["SlackInteractive"]


logging.getLogger("slack-interactive-lambda").addHandler(NullHandler())
