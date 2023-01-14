import json

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from starlette.config import Config

from models.people import People
from security.auth import AuthHandler
from security.schemas import AuthDetails

auth_handler = AuthHandler()
users = []

config = Config('.env')
file = config.get("file")
app = FastAPI()

people_list = []
with open(file, 'r') as json_file:
    people_data = json.loads(json_file.read())
    for p in people_data:
        people_list.append(People(**p))


@app.get('/search/<username>', response_model=Page[People], status_code=200)
async def get_person_by_username(username, auth_user=Depends(auth_handler.auth_wrapper)):
    return paginate([x for x in people_data if x['username'] == username])


@app.get('/people', response_model=Page[People], status_code=200)
async def get_all_persons(auth_user=Depends(auth_handler.auth_wrapper)):
    return paginate(people_data)


@app.delete('/people/<username>', status_code=204)
async def delete_person_by_username(username, auth_user=Depends(auth_handler.auth_wrapper)):
    for x in people_data:
        if x['username'] == username:
            people_data.remove(x)
    return


@app.post('/register', response_model=None, status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return


@app.post('/login', status_code=202)
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


add_pagination(app)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
