[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Phish Telegram Bot

Commands:
Simply type `/` into Telegram when you are chatting with the bot or read `main()` of `app.py`

Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

Development:
* The [phish bot](https://github.com/shapiroj18/phish-bot) needs to be running via `docker-compose`
* Run `source start-dev-env.sh` to start virtual environment, log in to heroku and store local env variables.
* Run `python app.py` to start the local bot

Dependencies:
* [Python3](https://www.python.org/downloads/)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
* [`jq`](https://stedolan.github.io/jq/)

Testing:
From the project root, run `python -m pytest`

The environmental variables stored are:
1. BOT_TOKEN=`bot_token` (token for `@gone_phishing_bot` from BotFather)
2. BOT_USERNAME=`username` (username for `@gone_phishing_bot` from BotFather)
3. URL=`url` (url of heroku app)

Ideas:
1. Phish Trivia Game
2. Next Phish Show (location/date)

To Do:
It seems pretty difficult to write integration tests for telegram. The best article I could find on it was using [telethon](https://docs.telethon.dev/en/latest/index.html) and can be found [here](https://blog.1a23.com/2020/03/06/how-to-write-integration-tests-for-a-telegram-bot/).