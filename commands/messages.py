class Messages:
    
    def __init__(self) -> None:
        ...
    
    
    # Start message
    def start_message(self) -> str:
        """Initial Message"""
        message = """
        \U0001F420 Welcome to the Phish Bot! Send "/features" for bot commands!
        """
        
        return message