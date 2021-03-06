from curses import has_ic
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query
from app import models,dep
from app.config import settings

from hashids import Hashids

from app import schemas

hashids = Hashids(salt=settings.HASHIDS_SALT,min_length=7)

def get_user(db:Session,user_id:str):
    try:
        id=int(hashids.decode(user_id)[0])
    except:
        return None
    user = db.query(models.User).filter(models.User.id==id).first()
    if user:
        user_result = models.User(id=hashids.encode(user.id),username=user.username,hashed_password=user.hashed_password,is_student=user.is_student,is_family=user.is_family,is_active=user.is_active,password_expired=user.password_expired)
        return user_result
    else:
        return None
    

def get_user_by_name(db:Session,username:str):
    user = db.query(models.User).filter(models.User.username==username).first()
    if user:
        user_result = models.User(id=hashids.encode(user.id),username=user.username,hashed_password=user.hashed_password,is_student=user.is_student,is_family=user.is_family,is_active=user.is_active,password_expired=user.password_expired)
        return user_result
    else:
        return None

def get_all_users(db:Session):
    raw_users = db.query(models.User).all()
    users=[]
    for user in raw_users:
        user.id = hashids.encode(user.id)
        users.append(user)
    return users

def create_user(db:Session,user:schemas.UserCreate):
    hashed_password = dep.get_password_hash(user.password)
    db_user = models.User(username=user.username, is_family=False,is_active=False,password_expired=False,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_result = models.User(id=hashids.encode(db_user.id),username=db_user.username,hashed_password=db_user.hashed_password,is_student=db_user.is_student,is_family=db_user.is_family,is_active=db_user.is_active,password_expired=db_user.password_expired)
    return user_result

def create_user_by_admin(db:Session,user:schemas.UserCreateByAdmin):
    hashed_password = dep.get_password_hash(user.password)
    db_user = models.User(username=user.username, is_family=user.is_family,is_active=user.is_active,password_expired=user.password_expired,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_result = models.User(id=hashids.encode(db_user.id),username=db_user.username,hashed_password=db_user.hashed_password,is_student=db_user.is_student,is_family=db_user.is_family,is_active=db_user.is_active,password_expired=db_user.password_expired)
    return user_result

def change_password(db:Session,user:schemas.PasswordChange):
    db_user=db.query(models.User).filter(models.User.username==user.username).first()
    hashed_new_password = dep.get_password_hash(user.new_password)
    db_user.hashed_password=hashed_new_password
    db_user.password_expired=False
    db.commit()
    return user

def create_group(db:Session,group:schemas.GroupCreate):
    db_group = models.Group(groupname=group.groupname,title=group.title,description=group.description,page_content=group.page_content,enable_vote=group.enable_vote,twitter_url=group.twitter_url,instagram_url=group.instagram_url,stream_url=group.stream_url)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    group_result = models.Group(id=hashids.encode(db_group.id),groupname=db_group.groupname,title=db_group.title,description=db_group.description,page_content=db_group.page_content,enable_vote=db_group.enable_vote,twitter_url=db_group.twitter_url,instagram_url=db_group.instagram_url,stream_url=db_group.stream_url)
    return group_result
def get_all_groups(db:Session):
    db_groups = db.query(models.Group).all()
    groups=[]
    for group in db_groups:
        group.id = hashids.encode(group.id)
        groups.append(group)
    return groups
def get_group(db:Session,hashids_id:str):
    try:
        id=int(hashids.decode(hashids_id)[0])
    except:
        return None
    group = db.query(models.Group).filter(models.Group.id==id).first()
    if group:
        group_result = models.Group(id=hashids.encode(group.id),groupname=group.groupname,title=group.title,description=group.description,page_content=group.page_content,enable_vote=group.enable_vote,twitter_url=group.twitter_url,instagram_url=group.instagram_url,stream_url=group.stream_url,tags=group.tags)
        return group_result
    else:
        return None
def add_tag(db:Session,hashidsgroup_id:str,tag:schemas.GroupTagCreate):
    try:
        group_id=int(hashids.decode(hashidsgroup_id)[0])
        tag_id=int(hashids.decode(tag.tag_id)[0])
    except:
        return None
    db_group = db.query(models.Group).filter(models.Group.id==group_id).first()
    db_tag = db.query(models.Tag).filter(models.Tag.id==tag_id).first()
    db_group.tags.append(db_tag)
    '''
    group = get_group(db,hashidsgroup_id)
    group_result = models.Group(id=int(hashids.decode(group.id)[0]),groupname=group.groupname,title=group.title,description=group.description,page_content=group.page_content,enable_vote=group.enable_vote)
    db_tag = get_tag(db,tag.tag_id)
    tag = models.Tag(id=int(hashids.decode(db_tag.id)[0]),tagname=db_tag.tagname,groups=db_tag.groups)
    group_result.tags.append(tag)
    '''
    db.commit()
    return "Add Tag Successfully"


def create_event(db:Session,hashidsgroup_id:str,event:schemas.EventCreate):
    group = get_group(db,hashidsgroup_id) 
    if not group:
        return None
    try:
        group_id=int(hashids.decode(group.id)[0])
    except:
        return None
    if not (event.sell_at<event.sell_ends and event.sell_ends<event.starts_at and event.starts_at<event.ends_at):
        return None
    db_event = models.Event(title=event.title,description=event.description,sell_at=event.sell_at,sell_ends=event.sell_ends,starts_at=event.starts_at,ends_at=event.ends_at,ticket_stock=event.ticket_stock,lottery=event.lottery,group_id=group_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    event_result = models.Event(id=hashids.encode(db_event.id),title=db_event.title,description=db_event.description,sell_at=db_event.sell_at,sell_ends=db_event.sell_ends,starts_at=db_event.starts_at,ends_at=db_event.ends_at,ticket_stock=db_event.ticket_stock,lottery=db_event.lottery,group_id=hashids.encode(db_event.group_id))
    return event_result

def get_all_events(db:Session,hashidsgroup_id:str):
    try:
        group_id = int(hashids.decode(hashidsgroup_id)[0])
    except:
        return None
    db_events = db.query(models.Event).filter(models.Event.group_id==group_id).all()
    events=[]
    for event in db_events:
        event.id = hashids.encode(event.id)
        event.group_id = hashids.encode(event.group_id)
        events.append(event)
    return events
def get_event(db:Session,hashidsgroup_id:str,hashidsevent_id:str):
    try:
        group_id=int(hashids.decode(hashidsgroup_id)[0])
        event_id=int(hashids.decode(hashidsevent_id)[0])
    except:
        return None
    db_event = db.query(models.Event).filter(models.Event.group_id==group_id,models.Event.id==event_id).first()
    if db_event:
        event_result = models.Event(id=hashids.encode(db_event.id),title=db_event.title,description=db_event.description,sell_at=db_event.sell_at,sell_ends=db_event.sell_ends,starts_at=db_event.starts_at,ends_at=db_event.ends_at,ticket_stock=db_event.ticket_stock,lottery=db_event.lottery,group_id=hashids.encode(db_event.group_id))
        return event_result
    else:
        return None

## Tag CRUD
def create_tag(db:Session,tag:schemas.TagCreate):
    db_tag=models.Tag(tagname=tag.tagname)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    tag = models.Tag(id=hashids.encode(db_tag.id),tagname=db_tag.tagname)
    return tag
def get_all_tags(db:Session):
    db_tags=db.query(models.Tag).all()
    tags=[]
    for tag in db_tags:
        tag.id = hashids.encode(tag.id)
        tags.append(tag)
    return tags
def get_tag(db:Session,hashids_id:str):
    try:
        id=int(hashids.decode(hashids_id)[0])
        db_tag = db.query(models.Tag).filter(models.Tag.id==id).first()
    except:
        return None
    if db_tag:
        tag = models.Tag(id=hashids.encode(db_tag.id),tagname=db_tag.tagname)
        return tag
    return None
def put_tag(db:Session,hashids_id:str,tag:schemas.TagCreate):
    try:
        id=int(hashids.decode(hashids_id)[0])
        db_tag = db.query(models.Tag).filter(models.Tag.id==id).first()
    except:
        return None
    db_tag.tagname=tag.tagname
    db.commit()
    db.refresh(db_tag)
    tag_result = models.Tag(id=hashids.encode(db_tag.id),tagname=db_tag.tagname)
    return tag_result
def delete_tag(db:Session,hashids_id:str):
    try:
        id=int(hashids.decode(hashids_id)[0])
        db_tag = db.query(models.Tag).filter(models.Tag.id==id).first()
    except:
        return None
    db.delete(db_tag)
    db.commit()
    return 0




### ????????????(Admin??????????????????)

def grant_admin(db:Session,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return None
    db_admin = models.Admin(user_id=id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return "Grant Admin Successfully"

def grant_owner_of(db:Session,group:schemas.Group,user:schemas.User):
    try:
        group_id=int(hashids.decode(group.id)[0])
        user_id=int(hashids.decode(user.id)[0])
    except:
        raise HTTPException(400,"Invalid Parameter")
    #db_owner = models.Authority(user_id=user_id,group_id=group_id,role=schemas.AuthorityRole.Owner)
    #db.add(db_owner)
    #db.commit()
    #db.refresh(db_owner)
    user = db.query(models.User).filter(models.User.id==user_id).first()
    group = db.query(models.Group).filter(models.Group.id==group_id).first()
    user.groups.append(group)
    db.commit()
    return "Grant Owner Successfully"

def grant_authorizer_of(db:Session,group:schemas.Group,user:schemas.User):
    try:
        group_id=int(hashids.decode(group.id)[0])
        user_id=int(hashids.decode(user.id)[0])
    except:
        raise HTTPException(400,"Invalid Parameter")
    db_authorizer = models.Authority(user_id=user_id,group_id=group_id,role=schemas.AuthorityRole.Authorizer)
    db.add(db_authorizer)
    db.commit()
    db.refresh(db_authorizer)
    return "Grant Authorizer Successfully"

def check_admin(db:Session,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return False
    if not db.query(models.Admin).filter(models.Admin.user_id==id).first():
        return False
    return True

def check_owner_of(db:Session,group:schemas.Group,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return False
    if not db.query(models.Authority).filter(models.Authority.user_id==id,models.Authority.group_id==group.id,models.Authority.role==schemas.AuthorityRole.Owner).first():
        return False
    return True

def check_owner(db:Session,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return False
    if not db.query(models.Authority).filter(models.Authority.user_id==id,models.Authority.role==schemas.AuthorityRole.Owner).first():
        return False
    return True

def check_authorizer_of(db:Session,group:schemas.Group,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return False
    if not db.query(models.Authority).filter(models.Authority.user_id==id,models.Authority.group_id==group.id,models.Authority.role==schemas.AuthorityRole.Authorizer).first():
        return False
    return True

def check_authorizer(db:Session,user:schemas.User):
    try:
        id = int(hashids.decode(user.id)[0])
    except:
        return False
    if not db.query(models.Authority).filter(models.Authority.user_id==id,models.Authority.role==schemas.AuthorityRole.Authorizer).first():
        return False
    return True

