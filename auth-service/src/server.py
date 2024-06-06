import jwt, datetime, os
from zoneinfo import ZoneInfo
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from model.model import User
from schema.schema import UserSchema
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Everything seems ok"}

@app.post("/login", response_model=str)
async def login(user: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user.email).first()
    if not user or user.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = createJWT(user.email, JWT_SECRET, True)
    return token

@app.post("/validate", response_model=dict)
async def validate(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"username": payload["username"], "admin": payload["admin"]}

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=ZoneInfo('UTC')) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())