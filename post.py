from fastapi import APIRouter, Depends
import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel
import OAuth

# Database connection 
conn = psycopg.connect(host="localhost", dbname="FastApi", user="postgres", password="23042008", row_factory=dict_row)
cursor = conn.cursor()

router = APIRouter(tags=["Post"])

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@router.post("/post", status_code=201)
async def create_post(post: Post, current_user: int = Depends(OAuth.get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post, "current_user": current_user}
