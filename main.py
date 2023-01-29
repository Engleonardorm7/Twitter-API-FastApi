#Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import HTTPException
from fastapi.param_functions import Path

app=FastAPI()
app.title="Twetter API"
app.version="0.0.1"
#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class Userlogin(UserBase):#password se deja en clase aparte para prevenir fallas de seguridad
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
 
class User(UserBase):
    
    
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    birth_date: Optional[date]=Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
        )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


class LogOut(BaseModel):
    email: EmailStr = Field(...)
    message: str = Field(default=None)


# Path Operations

## Users

### Register a User
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user:UserRegister=Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        -Request body parameter
            -user: UserRegister

    Returns a Json with the basic user information:
        - user_id:UUID
        - email: Emailstr
        - first_name: str
        - last_name:str
        - birth_date: date
    """
    with open("users.json","r+", encoding="utf-8") as f:
        results=json.loads(f.read())#para convertir en una lista de diccionarios y que se pueda trabajar
        user_dict=user.dict()
        user_dict["user_id"]=str(user_dict["user_id"])
        user_dict["birth_date"]=str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)#Para volver al inicio del archivo nuevamente al byte 0, para que reemplace todo el contenido que ya estaba
        f.write(json.dumps(results)) #Para convertir nuevamente en un archivo tipo json
        return user

### Login a user
@app.post(
    path="/login",
    response_model=LogOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(email: EmailStr = Body(...),password: str=Body(...)):
    
    """
    Login

    This path operation allows a user to login in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    with open("users.json","r",encoding="utf-8") as f:
        datos = list(json.loads(f.read()))
        for user in datos:
            if email == user["email"] and password == user["password"]:
                return LogOut(email=email, message="Welcome, successful login!")
            
        
        return LogOut(email=email, message= "incorrect email or password")


###Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"]
)
def show_all_users():
    """
   This path operation shows all users in the app

   Parameters:
        -
    
    Returns a json list with all users in the app, with the following keys:
        - user_id:UUID
        - email: Emailstr
        - first_name: str
        - last_name:str
        - birth_date: date

    """
    with open("users.json","r",encoding="utf-8") as f:
        results=json.loads(f.read())
        return results


###Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id:str=Path(...)):
    """
   This path operation shows a user registered in the app by the ID

   Parameters:
        -user_id: str 
    
    Returns a json with the user's information: first_name, last_name, email, user_id, date_of_birth

    """
    with open("users.json","r",encoding="utf-8") as f:
        results=list(json.loads(f.read()))
        for user in results:
            if user_id==user["user_id"]:
                user=dict(user)
                return user
        if user_id != user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This user does not exist"
            )

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id:str=Path(...)):
    """
    Delete a user

    This path operation deletes a user 

    Parameters:
    - Request Body Parameters:
        - user_id: str
    
    Returns a json saying the user provided was succesfully deleted, if the user does not exists, the json will show it up to you

    """
    with open("users.json","r",encoding="utf-8") as f:
        results=list(json.loads(f.read()))
        for user in results:
            if user_id==user["user_id"]:
                results.remove(user)
                with open("users.json","w",encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return user

        if user_id != user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This user does not exist"
            )


#Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_id:str=Path(...), user:User=Body(...)):

    """
    Update a user

    This path operation Updates a user information

    Parameters:
    - Request Body Parameters:
        - user_id: str
    
    Returns a Json with User Json information with the new data given

    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = list(json.loads(f.read()))
        for user in results:
            if user["user_id"] == user_id:
                results[results.index(user)] = user_dict
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return user_dict
                
        if user_id != user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This user does not exist"
            )



## Tweets
###Show all the tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
    )
def home():
    """
   This path operation shows all tweets in the app

   Parameters:
        -
    
    Returns a json list with all tweets in the app, with the following keys:
        - tweet_id: UUID }
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 

    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results=json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet:Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters:
        -Request body parameter
            -tweet:Tweet

    Returns a Json with the basic Tweet information:
        - tweet_id: UUID }
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 
    """
    with open("tweets.json","r+", encoding="utf-8") as f:
        results=json.loads(f.read())#para convertir en una lista de diccionarios y que se pueda trabajar
        tweet_dict=tweet.dict()
        tweet_dict["tweet_id"]=str(tweet_dict["tweet_id"])
        tweet_dict["created_at"]=str(tweet_dict["created_at"])
        tweet_dict["updated_at"]=str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"]=str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"]=str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)#Para volver al inicio del archivo nuevamente al byte 0, para que reemplace todo el contenido que ya estaba
        f.write(json.dumps(results)) #Para convertir nuevamente en un archivo tipo json
        return tweet

### show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show(tweet_id:str=Path(...)):
    """
   This path operation shows a tweet posted in the app by the ID

   Parameters:
        -tweet_id: str 
    
    Returns a json with the tweets's information: tweet_id, Content, created_at, updated_at, Posted by

    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results=list(json.loads(f.read()))
        for tweet in results:
            if tweet_id==tweet["tweet_id"]:
                tweet=dict(tweet)
                return tweet
        if tweet_id != tweet["tweet_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tweet does not exist"
            )

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id:str=Path(...)):
    """
    Delete a tweet

    This path operation deletes a tweet 

    Parameters:
    - Request Body Parameters:
        - tweet_id: str
    
    Returns a json saying the user provided was succesfully deleted, if the user does not exists, the json will show it up to you

    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results=list(json.loads(f.read()))
        for tweet in results:
            if tweet_id==tweet["tweet_id"]:
                results.remove(tweet)
                with open("tweets.json","w",encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return tweet

        if tweet_id != tweet["tweet_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This tweet does not exist"
            )

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(tweet_id:str=Path(...), tweet:Tweet=Body(...)):

    """
    Update a tweet

    This path operation Updates a tweet 

    Parameters:
    - Request Body Parameters:
        - tweet_id: str -> Tweet's ID 
        - tweet: tweet -> tweet object wich contains first_name, last_name, date_of_birth, used_id and email
    
    Returns a Json with Tweet Json information with the new data given

    """
    tweet_id = str(tweet_id)
    tweet_dict = tweet.dict()
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"] = str (tweet_dict["by"]["user_id"])
    tweet_dict["by"]["birth_date"] = str (tweet_dict["by"]["birth_date"])
    
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = list(json.loads(f.read()))
        for tweet in results:
            if tweet["tweet_id"] == tweet_id:
                results[results.index(tweet)] = tweet_dict
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                return tweet_dict
                
        if tweet_id != tweet["tweet_id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This user does not exist"
            )
