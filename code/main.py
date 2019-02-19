import os

from bot_creator import BotCreator
from handler import Handler


def main():
    app = BotCreator(os.environ["X_BOT_TOKEN"])
    handler = Handler(logger=app.logger)

    app.config_handlers(handler)
    print("Running!")
    app.run()


if __name__ == '__main__':
    main()
