from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from client.utilities.database import SessionLocal, User

app = FastAPI()

class UserRegister(BaseModel):
    username: str
    display_name: str
    pub_key: str

class CreateGroup(BaseModel):
    creator: str
    members: List[str]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Chat Server Online"}

@app.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    new_user = User(username=user.username,
        display_name=user.display_name,
        pub_key=user.pub_key)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.username} has been registered"}

@app.get("/search/{username}")
async def search_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
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
        user = db.query(User).filter(User.username == member).first()
        if user:
            keys[member] = user.pub_key
        else:
            keys[member] = "N/A"
    return {"group_members": keys}