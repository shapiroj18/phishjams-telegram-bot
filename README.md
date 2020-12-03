# Phish Telegram Bot

The bot is called `@gone_phishing_bot`

Deployed at `https://phish-telegram-bot.herokuapp.com/`

Commands:
1. `PHISH <YEAR>` returns a random phish jam from that year

Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

The environmental variables stored are:
1. BOT_TOKEN=`bot_token`
2. BOT_USERNAME=`username`
3. URL=`url`

There is a gitignore for `instance/`. In this folder lives a file called `config.py` that holds credentials with the format:
```
API_KEY= <API_KEY>
OTHER_API_KEY= <API_KEY>
```