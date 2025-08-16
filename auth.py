from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import psycopg
from psycopg.rows import dict_row
from utils import hash, verify
from OAuth import create_access_token

conn = psycopg.connect(host="localhost", dbname="FastApi", user="postgres", password="23042008", row_factory=dict_row)
cursor = conn.cursor()

router = APIRouter(tags=["Auth"])

@router.post("/sign-up")
async def sign_up(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("""SELECT * FROM jwt_test WHERE username = %s""", (user_credentials.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    cursor.execute("""INSERT INTO jwt_test (username, password) VALUES (%s, %s) 
                   RETURNING *""", (user_credentials.username, hash(user_credentials.password)))
    new_user = cursor.fetchone()
    conn.commit()
    return {"new user": new_user}


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("""SELECT * FROM jwt_test WHERE username = %s""", (user_credentials.username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    if not verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect user credentials")
    
    access_token = create_access_token({"user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}