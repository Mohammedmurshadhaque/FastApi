#Build the docker image
docker build -t persona_api .

#Run a container from docker iamge
docker container run --publish 80:80 --name persona_api persona_api

#Access the swagger/openapi UI
http://localhost/docs#/

#Create a user
POST /register

#Login using username & password to get JWT access token
POST /login

#Authorize using the JWT token in swagger/openapi UI(Top right corner)

#Get all persons
GET /people

#Get a person by username
GET /search/<username>

#Delete a person by username
DELETE /people/<username>
