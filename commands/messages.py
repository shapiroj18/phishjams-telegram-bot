import os

class Messages:
    
    def __init__(self) -> None:
        ...
    
    
    # Start message
    def start_message(self) -> str:
        """Initial Message"""
        message = f"""\U0001F420 Welcome to the Phish Bot! Send /features for bot commands!"""
        
        return message
    
    def features_message(self):
        """Features of bot"""
        heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
        message = f"""
        You can send me commands like:
        /queue (let's you add a random or specific jam to the online player: {heroku_flask_url})
        /randomjam (sends a random Phish jam)
        /subscribedailyjam (random daily jam emails)
        /unsubscribedailyjam (remove daily jam emails)
        /subscribemjm (reminder when mystery jam monday is posted)
        /unsubscribemjm (remove MJM reminders)
        /code (links to code repositories and contributing)
        /help (help menu)
        """
        
        return message
        
    def help_message(self):
        """Features of bot"""
        message = f"""Type /features for full bot commands."""
        
        return message