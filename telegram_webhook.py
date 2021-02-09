# this only needs to be run once per webhook
# docs found here - https://core.telegram.org/bots/api#setwebhook

import os
import json
import httpx


def set_local_webhook():
    payload = {
        "url": f'https://a135e8f8e559.ngrok.io/{os.environ.get("TELEGRAM_BOT_TOKEN")}'
    }

    # set webhook
    url = (
        f'https://api.telegram.org/bot{os.environ.get("TELEGRAM_BOT_TOKEN")}/setWebhook'
    )
    r = httpx.get(url, params=payload)
    print(json.dumps(r.json(), indent=4))

    if r.json()["ok"] == True:
        return "Webhook set"

    else:
        return "Error setting webhook"


def view_local_webhook_info():

    # set webhook
    url = f'https://api.telegram.org/bot{os.environ.get("TELEGRAM_BOT_TOKEN")}/getWebhookInfo'
    r = httpx.get(url)
    print(json.dumps(r.json(), indent=4))


if __name__ == "__main__":
    # set_local_webhook()
    view_local_webhook_info()
