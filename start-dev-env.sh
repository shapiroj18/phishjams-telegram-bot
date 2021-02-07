#!/usr/bin/env bash

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
        -p|--phish)
        if [[ $(brew help) ]]; then

            if [[ $(brew ls --versions figlet) ]]; then
                figlet -f bulbhead "phish bot"
            else
                echo 'Installing Figlet via Homebrew'
                brew install figlet
                figlet -f bulbhead "phish bot"
            fi

        else
            echo 'Install Homebrew if you want fun features at brew.sh'
        fi
        shift
        ;;
    esac
done