from fastapi import FastAPI
import db
import uvicorn
import os


app = FastAPI()


@app.post("/send_message")
def send_message(sender_id: int, receiver_id: int, text: str):
    db.send_message(sender_id, receiver_id, text)


@app.get("/read_messages")
def read_messages(user1_id: int, user2_id: int):
    db.read_messages(user1_id, user2_id)


@app.post("/set_online")
def set_online(user_id: int):
    db.set_online(user_id)


@app.get("/is_online")
def is_online(user_id: int):
    db.is_online(user_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=os.environ.get("port"), reload=True)
