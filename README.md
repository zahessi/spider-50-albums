# Music bot & scraper

This project includes 3 Docker containers: MySQL database, Telegram bot which offers you random album from the latest Pitchfork reviews or random album from Pitchfork's "50 best of 2018" albums and a scraper.

Running version is available at @zahessi_music_bot in Telegram.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Since the bot uses the polling for responding to the request, you don't need to get a specific URL and SSL certificate to run it.

### Prerequisites

For running you will need to get Docker and Docker-Compose (18.09.2-ce and 1.23.2 versions respectively recommended for smooth work).

Also you will need to create `.env` file in the root of the project consisting of:
```
X_BOT_TOKEN=your_token_of_the_bot
``` 
You can get this token from @BotFather in Telegram
### Installing

Considering you are in the root directory of the project and the Docker service is running:

```
docker-compose up
```

After this command bot, scraper and the database services are running. You can access the data via `/help`, `/latest_albums` and `/album50` commands. Once an hour the scraping job is done to retrieve new records and write them into the database.

## Built With

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Python interface for the Telegram Bot API.
* [Scrapy](https://github.com/scrapy/scrapy) - Fast high-level web crawling & scraping framework for Python.

## Authors

* **Alexandra Rievva** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

