# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from .database import SessionLocal, User

app = FastAPI()

user_directory: Dict[str, str] = {}

class UserRegister(BaseModel):
    username: str
    display_name: str
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
    user_directory[user.username] = user.pub_key
    return {"message": f"User {user.username} registered successfully"}

@app.get("/search/{username}")
async def search_user(username: str, db: Session = Depends(get_db)):
    user = dq.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {
        "username": user.username,
        "display_name": user.display_name,
        "pub_key": user.pub_key
    }

@app.post("/group/begin")
async def begin_group(group: CreateGroup):
    keys = {}
    for member in group.members:
        if member in user_directory:
            keys[member] = user_directory[member]
        else:
            keys[member] = "Not Found"
    return {"group_members": keys}