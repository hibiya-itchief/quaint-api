from datetime import datetime
from typing import List, Union
from fastapi import Query
from enum import Enum

from pydantic import BaseModel

class AuthorityRole(str,Enum):
    Authorizer = "Authorizer"
    Owner = "Owner"
    Admin = "Admin"

class EventBase(BaseModel):
    title:str=Query(max_length=200)
    description:str=Query(max_length=200)
    sell_at:datetime
    sell_ends:datetime
    starts_at:datetime
    ends_at:datetime
    ticket_stock:int
    lottery:bool=False
class EventCreate(EventBase):
    pass
class Event(EventBase):
    id:str#hashids
    group_id:str#hashids
    class Config:
        orm_mode=True
class EventAdmin(Event):
    tickets:List['Ticket']#Ticketのリストに一般ユーザーはアクセスできない方がいい
    class Config:
        orm_mode=True

class GroupBase(BaseModel):#hashidsのidをURLにする。groupnameは表示名
    groupname:str = Query(max_length=200)
    title:Union[str,None] = Query(default=None,max_length=200)
    description:Union[str,None] = Query(default=None,max_length=200)
    page_content:Union[str,None] = Query(default=None,max_length=16000)
    enable_vote:bool = True
    twitter_url:Union[str,None]=Query(default=None,regex="https?://twitter\.com/[0-9a-zA-Z_]{1,15}/?")
    instagram_url:Union[str,None]=Query(default=None,regex="https?://instagram\.com/[0-9a-zA-Z_.]{1,30}/?")
    stream_url:Union[str,None]=Query(default=None,regex="https?://web.microsoftstream\.com/video/[\w!?+\-_~=;.,*&@#$%()'[\]]+/?")
class GroupCreate(GroupBase):
    pass
class Group(GroupBase):
    id:str#hashids
    tags:List['Tag']
    events:List['Event']
    class Config:
        orm_mode=True

class GroupTagCreate(BaseModel):
    tag_id:str

class TagBase(BaseModel):
    tagname:str=Query(max_length=200)
class TagCreate(TagBase):
    pass
class Tag(TagBase):
    id:str#hashids
    #groups:List['Group']
    class Config:
        orm_mode=True

class TicketBase(BaseModel):
    event_id:str#hashids
    owner_id:str#hashids
    is_family_ticket:bool = False
    person:int = Query(default=1)#一緒に入場する人数(１人１チケットになったらこれを削除すればdbのdefaultが効く)
class TicketCreate(TicketBase):
    pass
class Ticket(TicketBase):
    id:str#hashids
    created_at:int
    is_used:bool

    events:List['Event']
    owner:List['User']
    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):#JWTに含まれるデータ
    username: Union[str,None] = None

class UserBase(BaseModel):
    username: str = Query(regex="^[a-zA-Z0-9_\-.]{3,15}$",min_length=4,max_length=25)
class UserCreate(UserBase):
    password: str=Query(min_length=8,regex="^[0-9a-zA-Z]*$",max_length=255)
class UserCreateByAdmin(UserCreate):
    is_student:bool=False
    is_family:bool=False
    is_active:bool=False
    password_expired: bool=True
class User(UserBase):
    id : str#hashids
    
    is_student:bool=False
    is_family:bool=False
    is_active:bool=False
    password_expired: bool=True

    
    groups: List['Group']=[]
    votes: List['Vote']=[]
    tickets: List['Ticket']=[]

    class Config:
        orm_mode=True

class PasswordChange(UserCreate):
    new_password:str=Query(min_length=6,regex="^[0-9a-zA-Z]*$",max_length=255)


class VoteModel(BaseModel):
    group_id:str#hashids
    user_id:str#hashids
class Vote(VoteModel):
    id:str#hashids


Event.update_forward_refs()
EventAdmin.update_forward_refs()
Group.update_forward_refs()
Tag.update_forward_refs()
Ticket.update_forward_refs()
User.update_forward_refs()

