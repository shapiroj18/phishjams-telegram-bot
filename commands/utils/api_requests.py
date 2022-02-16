import httpx

class APIRequests:
    def __init__(self):
        ...
        
    def basic_post(self, data, url):
        r = httpx.post(url, data=data)
        return r.json()
    
    def post_subscribe_daily_jams(self, heroku_flask_url, email, chat_id):

        response = self.basic_post(
            url = f"{heroku_flask_url}/subscribedailyjams", 
            data = {"email": email, "platform": "Telegram", "chat_id": chat_id}
        )
        
        print(f"flask response: {response}")

        message_response = response["message"]
        
        return message_response
    
    def post_unsubscribe_daily_jams(self, heroku_flask_url, email):

        response = self.basic_post(
            url = f"{heroku_flask_url}/unsubscribedailyjams", 
            data = {"email": email, "platform": "Telegram"}
        )
        print(f"flask response: {response}")

        message_response = response["message"]
        return message_response
    
    def post_subscribe_mjm(self, heroku_flask_url, chat_id):
        data = {
            "platform": "Telegram", "chat_id": chat_id
        }
        
        response = self.basic_post(
            url = f"{heroku_flask_url}/subscribemjm", data=data
        )
        print(f"flask response: {response}")
        message_response = response["message"]
        return message_response
    
    def post_unsubscribe_mjm(self, heroku_flask_url, chat_id):
        data = {
            "chat_id": chat_id
        }
        
        response = self.basic_post(
            url = f"{heroku_flask_url}/unsubscribemjm", data=data
        )
        print(f"flask response: {response}")
        message_response = response["message"]
        return message_response