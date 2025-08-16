from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import schemas, auth, post
from typing import List

conn = psycopg.connect(host="fake", dbname="fake", user="fake", password="fake", row_factory=dict_row)
cursor = conn.cursor()

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)

@app.get("/", response_model=List[schemas.Response])
def see_all():
    cursor.execute("""SELECT * FROM jwt_test""")
    users = cursor.fetchall()
    return [schemas.Response(**user) for user in users]

