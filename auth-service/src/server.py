import jwt, datetime, os
from fastapi import FastAPI, HTTPException, Depends, status, Header
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.model.model import User
from src.schema.schema import UserSchema
from dotenv import load_dotenv
from typing import Annotated

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
async def validate(authorization: Annotated[str, Header()], db: Session = Depends(get_db)):
    encoded_jwt = authorization.split(" ")[1]
    try:
        payload = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"username": payload["username"], "admin": payload["admin"]}

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())