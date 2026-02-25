from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from db import Database
import hashlib
import os
import uvicorn
import requests
from dotenv import load_dotenv


app = FastAPI()
db = Database()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt.hex() + ":" + dk.hex()


def _verify_password(stored: str, password: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split(":")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return dk.hex() == dk_hex


@app.post("/register")
def register(username: str, password: str, email: str):
    existing = db.get_user_by_username(username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username already used")
    
    hash_password = _hash_password(password)
    created = db.create_user(username, email, hash_password)

    if not created:
        raise HTTPException(status_code=500, detail="Failed to create account. Please try again later")
    
    return {"status": "success"}


@app.post("/login")
def login(username: str, password: str):
    user = db.get_user_by_username(username)
    
    if not user or "password" not in user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
    if not _verify_password(user["password"], password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")

    # remove password_hash for response
    requests.post(f"{os.environ.get("chat_service")}/set_online?user_id={user["id"]}")
    return {"status": "success", "user_id": user["id"]}


# @app.post("/logout")
# def logout(user_id: int):
#     try:
#         print(f"Logout user_id: {user_id}, type: {type(user_id)}")
#         return {"message": "Logged out"}
#     except Exception as e:
#         raise


@app.get("/profile")
def profile(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


if __name__ == "__main__":
    port = os.environ.get("fastapi_host")
    print(port)
    print(type(port))
    uvicorn.run(
            "main:app", host=os.environ.get("fastapi_host"), port=int(os.environ.get("fastapi_port")), reload=True, log_level="debug"
    )
