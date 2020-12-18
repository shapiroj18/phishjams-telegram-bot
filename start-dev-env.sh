#!/usr/bin/env bash

# pull environmental variables for config. -s denotes as shell format. will require login if you aren't logged in to cli.
# sed replaces "'" with nothing
export `heroku config -s --app=phish-telegram-bot | sed 's/'"'"'//g'`

# set up venv
{
if [[ "$VIRTUAL_ENV" != "" ]]
then
    deactivate
    python3 -m venv ./phish_bot && . ./phish_bot/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
else
    python3 -m venv ./phish_bot && . ./phish_bot/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
fi
} &> /dev/null

# flags (this is useful: https://pretzelhands.com/posts/command-line-flags)
for arg in "$@"
do
    case "$arg" in
        -r|--run)
        flask run
        shift
        ;;
    esac
done