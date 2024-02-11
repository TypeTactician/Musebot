import time
import json
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile
import requests
import functools

def add_api_key(func):
    @functools.wraps(func)
    def wrapper_with_api_key(self, *args, **kwargs):
        if not hasattr(self, 'headers'):
            self.headers = {'X-API-Key': self.api_key}
        return func(self, *args, **kwargs)
    return wrapper_with_api_key

class RESTApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
    
    @add_api_key
    def create_chat(self) -> str:
        res = requests.get(f"{self.base_url}/create_chat", headers=self.headers)
        if res.status_code == 200:
            response_data = res.json()
            chat_id = response_data["data"]["chat_id"]
            return chat_id
        else:
            raise Exception(f"Cannot create chat. Response {res.text}")

    @add_api_key
    def get_assistant_response(self, prompt: str, chat_id: str, files: List[UploadedFile]):
        url = f"{self.base_url}/get_response"

        # Prepare the files for upload
        file_uploads = [("files", (file.name, file, file.type)) for file in files] if files else []
        # print(f"{file_uploads = }")

        # Send the POST request with both JSON data and files
        res = requests.post(url, headers=self.headers, data={'chat_id': chat_id, 'message': prompt, 'role': 'user'}, files=file_uploads)

        # Process the response
        if res.status_code == 200:
            response_data = res.json()
            message_data = response_data["data"]["message_data"]
            return message_data
        else:
            # print(f"{res.request.headers = }")
            # print(f"{res.request.body = }")
            raise Exception(f"Couldn't get response from assistant. Response: {res.text}")
