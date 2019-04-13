import inspect

import telegram

import db_connector
import settings, message_formatter


def process_album(func):
    def wrapper(*args):
        self = args[0]
        update = args[1]

        self.logger.info(f"User {update.message.chat_id} requested '/{inspect.stack()[1].function}'")
        model = func(*args)
        update.message.reply_text(text=self.formatter.create_message_for_album(model),
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    return wrapper


class Handler:

    def __init__(self, logger):
        self.logger = logger
        self.db = db_connector.DBconnector(config=settings.db_config)
        self.formatter = message_formatter.MessageFormatter()

    def _get_functions(self):
        for pair in inspect.getmembers(self, predicate=inspect.ismethod):
            if pair[0][0] != "_":
                yield pair

    def start(self, bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, bot, update):
        """Show this message"""
        text = '\n'.join([f"/{name} - {function.__doc__}" for name, function in self._get_functions()])
        update.message.reply_text(text)

    def latest_albums(self, bot, update):
        """select random album from 50 latest reviews on the Pitchfork"""
        self._get_random_by_tag(update, "latest")

    def album50(self, bot, update):
        """select random album from Pitchfork "Best of 2018 albums" """
        self._get_random_by_tag(update, "50_2018")

    def pure_random(self, bot, update):
        """select purely random album from pitchfork"""
        self._get_pure_random(update)

    @process_album
    def _get_random_by_tag(self, update, tag):
        return self.db.get_random_album(tag)

    @process_album
    def _get_pure_random(self, update):
        return self.db.select_pure_random()

    # def _get_album(self, update, tag):
    #     self.logger.info(f"User {update.message.chat_id} requested '/{inspect.stack()[1].function}'")
    #     model =
    #     update.message.reply_text(text=self.formatter.create_message_for_album(model),
    #                               parse_mode=telegram.ParseMode.MARKDOWN)
