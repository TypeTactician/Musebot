from openai import OpenAI
import streamlit as st
from src.utils import RESTApiClient

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
CHATBOT_NAME = "Riwa-AI"
HOST = "http://104.238.180.27:8000"
REST_API_KEY = "ebd5d852-df11-4b31-941b-22439c9356a3"
ACCEPTED_FILE_TYPES = ["pdf", "txt", "png", "jpeg", "jpg"]

# print(HOST, REST_API_KEY)
client = RESTApiClient(HOST, REST_API_KEY)

st.title(CHATBOT_NAME)

if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = client.create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

# This will load initial messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Upload files form (this moves as chat messages adds up... And also if you attach a file, then you keep it in next massages. You should fix it) - TEMP - IMPR
with st.form("Files form", clear_on_submit=True):
    # uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, type=ACCEPTED_FILE_TYPES)
    uploaded_files = [st.file_uploader("Upload Files", accept_multiple_files=False, type=ACCEPTED_FILE_TYPES)]        # You could accept multiple files in theory but Assistants have problems, with two files, you can only read the second... https://community.openai.com/t/how-to-use-multiple-files-in-assistants-api/514741
    submitted = st.form_submit_button("Attach")

    if submitted:
        st.write("Files attached to next message! Type something!")

prompt = st.chat_input("Write your message here...")

if prompt:
    uploaded_files = [file for file in uploaded_files if file is not None]     # This is useful only is you're using accept_multiple_files=False instead of accept_multiple_files=True in st.file_uploader

    with st.chat_message("user"):
        st.markdown(prompt)
        st.write(f"Attached files: {', '.join([file.name for file in uploaded_files])}")

    with st.chat_message("assistant"):
        response = client.get_assistant_response(prompt, st.session_state.chat_id, uploaded_files)
        st.markdown(response['message'])

    st.session_state.messages.append({"role": "user", "content": prompt, "files": uploaded_files})
    st.session_state.messages.append({"role": "assistant", "content": response['message'], "files": []})           # For now, the assistant never outputs files

    # Reset uploaded_files to None after processing the user's message
    st.session_state.uploaded_files = None
