from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


@app.get("/blog")
def root(limit, published: bool = False, sort: Optional[str] = None):
    if published is True:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/{id}")
def show(pk: int):
    return {"data": pk}


@app.get('/blog/{pk}/comments/')
def comments(pk: int, limit=10):
    return limit
    return {"data": {pk, 'comment1', 'comment2'}}
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {"data": f'Blog is created with title as {request.title}'}


