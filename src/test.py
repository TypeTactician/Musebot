from utils import RESTApiClient
import requests

client = RESTApiClient("http://104.238.180.27:8000", "ebd5d852-df11-4b31-941b-22439c9356a3")

chat_id = client.create_chat()
# client.get_assistant_response("Hello, who are you?", chat_id, files={"files": ()})