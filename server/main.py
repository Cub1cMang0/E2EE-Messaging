# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

user_directory: Dict[str, str] = {}

class UserRegister(BaseModel):
    usermame: str
    pub_key: str

class CreateGroup(BaseModel):
    creator: str
    members: List[str]

@app.get("/")
def read_root():
    return {"status": "Chat Server Online"}

@app.post("/register")
async def register_user(user: UserRegister):
    if user.username in user_directory:
        raise HTTPException(status_code=400, detail="Username already taken")
    user_directory[user.usermame] = user.pub_key
    return {"message": f"User {user.usermame} registered successfully"}

@app.get("/search/{username}")
async def search_user(username: str):
    if username not in user_directory:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {"username": username, "pub_key": user_directory[username]}

@app.post("/group/begin")
async def begin_group(group: CreateGroup):
    keys = {}
    for member in group.members:
        if member in user_directory:
            keys[member] = user_directory[member]
        else:
            keys[member] = "Not Found"
    return {"group_members": keys}