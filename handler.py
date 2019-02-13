import inspect

import telegram

from pitchfork_parse.pitchfork_parse import db_connector
import settings
import message_formatter


class Handler:

    def __init__(self, logger):
        self.logger = logger
        self.db = db_connector.DBconnector(config=settings.db_config)
        self.formatter = message_formatter.MessageFormatter()

    def get_functions(self):
        for pair in inspect.getmembers(self, predicate=inspect.ismethod):
            if pair[0] not in ["__init__", "get_functions", "_get_album"]:
                yield pair

    def start(self, bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, bot, update):
        """Show this message"""
        text = '\n'.join([f"/{name} - {function.__doc__}" for name, function in self.get_functions()])
        update.message.reply_text(text)

    def latest_albums(self, bot, update):
        """select random album from latest reviews on the Pitchfork"""
        self._get_album("latest", update)

    def album50(self, bot, update):
        """select random album from Pitchfork "Best of 2018 albums" """
        self._get_album("50_2018", update)

    def _get_album(self, tag, update):
        self.logger.info(f"User {update.message.chat_id} requested '/{inspect.stack()[1].function}'")
        model = self.db.get_random_album(tag)
        update.message.reply_text(text=self.formatter.create_message_for_album(model),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
