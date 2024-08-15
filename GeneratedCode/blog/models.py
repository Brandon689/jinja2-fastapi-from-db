from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsersBase(BaseModel):
    Username: str
    Email: str
    PasswordHash: str
    CreatedAt: str
    IsAdmin: bool
    

class UsersCreate(UsersBase):
    pass

class Users(UsersBase):
    Id: int

class CategoriesBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    

class CategoriesCreate(CategoriesBase):
    pass

class Categories(CategoriesBase):
    Id: int

class PostsBase(BaseModel):
    Title: str
    Content: str
    CreatedAt: str
    UpdatedAt: Optional[datetime] = None
    AuthorId: int
    CategoryId: int
    

class PostsCreate(PostsBase):
    pass

class Posts(PostsBase):
    Id: int

class CommentsBase(BaseModel):
    Content: str
    CreatedAt: str
    PostId: int
    UserId: int
    

class CommentsCreate(CommentsBase):
    pass

class Comments(CommentsBase):
    Id: int

