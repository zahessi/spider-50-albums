from telegram.ext import Updater, CommandHandler
import logging


# добавить логер, который будет писать чат айди и какую команду, добавить лог на ошибки и лог на крон таску

class BotCreator(Updater):

    def __init__(self, token):
        super().__init__(token=token)
        self.dp = self.dispatcher

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def run(self):
        self.start_polling()
        self.idle()

    def _error_handler(self, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def config_handlers(self, handler):
        for name, function in handler.get_functions():
            self.dp.add_handler(CommandHandler(name, function))
        self.dp.add_error_handler(self._error_handler)
