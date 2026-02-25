import os
from typing import Optional
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)


USER_SERVICE = os.environ.get("user_service")
CHAT_SERVICE = os.environ.get("chat_service")
DOC_SERVICE = os.environ.get("doc_service")


@app.post("/login")
def login(username: str, password: str):
    response = requests.post(f"{USER_SERVICE}/login?username={username}&password={password}")
    return response.json()


@app.post("/register")
def register(username: str, password: str, email: str):
    response = requests.post(f"{USER_SERVICE}/register?username={username}&password={password}&email={email}")
    return response.json()


@app.post("/create_doc")
def create_doc(doc: Optional[dict], doc_path: Optional[str]):
    requests.post(f"{DOC_SERVICE}/update_doc?doc={doc}&doc_path={doc_path}")


@app.put("/update_doc")
def update_doc(doc_id, key: str, new_value):
    requests.put(f"{DOC_SERVICE}/update_doc?doc_id={doc_id}&key={key}&new_value={new_value}")


@app.get("/get_doc")
def get_doc(doc_id):
    requests.get(f"{DOC_SERVICE}/get_doc?doc_id={doc_id}")


@app.post("/send_message")
def send_message(sender_id: int, receiver_id: int, text: str):
    requests.post(f"{CHAT_SERVICE}/send_message?sender_id={sender_id}&receiver_id={receiver_id}&text={text}")


@app.get("/read_messages")
def read_messages(user1_id: int, user2_id: int):
    requests.get(f"{CHAT_SERVICE}/read_messages?user1_id={user1_id}&user2_id={user2_id}")


@app.post("/set_online")
def set_online(user_id: int):
    requests.post(f"{CHAT_SERVICE}/set_online?user_id={user_id}")


@app.post("/logout")
def logout(user_id: int):
    response = requests.post(f"{CHAT_SERVICE}/set_offline?user_id={user_id}")
    return response.json()


@app.get("/is_online")
def is_online(user_id: int):
    response = requests.get(f"{CHAT_SERVICE}/is_online?user_id={user_id}")
    return response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=int(os.environ.get("port")), reload=True)

