from commands.base_commands import BaseCommands
from commands.messages import Messages

class FinalCommands:
    
    def __init__(self) -> None:
        # load libraries
        self.basic_commands = BaseCommands()
        self.messages = Messages()
    
    
    # Start message
    def start(self, update, context) -> None:
        message = self.messages.start_message()
        self.basic_commands.send_basic_message(update, context, message)
        
    def features(self, update, context) -> None:
        message = self.messages.features_message()
        self.basic_commands.send_basic_message(update, context, message)
        
    def help(self, update, context) -> None:
        message = self.messages.help_message()
        self.basic_commands.send_basic_message(update, context, message)