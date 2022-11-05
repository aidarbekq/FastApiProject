from typing import List

from pydantic import BaseModel


class Users(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    title: str
    body: str

    class Config():
        orm_mode = True
class ShowUsers(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config():
        orm_mode = True




class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUsers

    class Config():
        orm_mode = True
        