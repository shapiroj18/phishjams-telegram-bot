import os
import pytest
from dotenv import load_dotenv
from commands.bot_functionality.base_commands import BaseCommands

load_dotenv()

base_commands = BaseCommands()


def test_create_inline_keyboard_no_error():
    # should not have an error
    base_commands.create_inline_keyboard(buttons=["foo", "bar"], urls=[None, "random.org"])

def test_create_inline_keyboard_error():
    # should have an error
    with pytest.raises(RuntimeError):
        base_commands.create_inline_keyboard(buttons=["foo", "bar"], urls=["random.org"])
