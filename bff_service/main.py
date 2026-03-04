import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import jwt
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


def id_from_jwt(encoded_jwt: str) -> dict:
    decoded_jwt = jwt.decode(encoded_jwt, "secret", algorithms="HS256")
    return decoded_jwt["user_id"]


@app.post("/login")
def login(username: str, password: str):
    response = requests.post(
        f"{USER_SERVICE}/login?username={username}&password={password}"
    )
    return response.json()


@app.get("/check_role")
def check_role(user_token: str, role_id: int):
    user_id = id_from_jwt(user_token)
    response = requests.get(
        f"{USER_SERVICE}/check_role?user_id={user_id}&role_id={role_id}"
    )
    return response.json()


@app.post("/register")
def register(username: str, password: str, email: str):
    response = requests.post(
        f"{USER_SERVICE}/register?username={username}&password={password}&email={email}"
    )
    return response.json()


@app.post("/create_doc")
async def create_doc(request: Request):
    doc = await request.json()
    response = requests.post(f"{DOC_SERVICE}/create_doc", json=doc)
    return response.json()


@app.put("/update_doc")
def update_doc(doc_id, key: str, new_value):
    response = requests.put(
        f"{DOC_SERVICE}/update_doc?doc_id={doc_id}&key={key}&new_value={new_value}"
    )
    return response.json()


@app.get("/get_doc")
def get_doc(doc_id):
    response = requests.get(f"{DOC_SERVICE}/get_doc?doc_id={doc_id}")
    return response.json()


@app.post("/send_message")
def send_message(user_token: str, receiver_id: int, text: str):
    sender_id = id_from_jwt(user_token)
    response = requests.post(
        f"{CHAT_SERVICE}/send_message?sender_id={sender_id}&receiver_id={receiver_id}&text={text}"
    )
    return response.json()


@app.get("/read_messages")
def read_messages(user_token: str, user2_id: int):
    user1_id = id_from_jwt(user_token)
    response = requests.get(
        f"{CHAT_SERVICE}/read_messages?user1_id={user1_id}&user2_id={user2_id}"
    )
    return response.json()


@app.post("/logout")
def logout(user_token: str):
    user_id = id_from_jwt(user_token)
    response = requests.post(f"{CHAT_SERVICE}/set_offline?user_id={user_id}")
    return response.json()


@app.get("/is_online")
def is_online(user_token: str):
    user_id = id_from_jwt(user_token)
    response = requests.get(f"{CHAT_SERVICE}/is_online?user_id={user_id}")
    return response.json()


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=int(os.environ.get("port")), reload=True
    )
