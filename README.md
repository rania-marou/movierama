# MovieRama

MovieRama is a social sharing platform where users can share their favorite movies. Each movie has a title and a small description as well as a date that corresponds to the date it was added to the database. In addition it holds a reference to the user that submitted it. Users can also express their opinion about a movie by either likes or hates.

## Technical details

### Frameworks
MovieRama is web application that consists of a RESTful API and a simple user interface that consumes it.
The API is built with the Django REST Framework and uses Sqlite as database storage.
The User Interface is build with the Bootstrap Framework and is being served through the Django Framework.

### Authentication
The API is using JSON Web Tokens to authenticate requests.

## Running instructions

There are two ways to run the application, either using docker or by running the code locally.

Ensure the codebase has been cloned and that you navigate to the project's folder, running the commands:

```
git clone https://github.com/rania-marou/movierama
cd movierama
```

Once the application is up and running (by following the steps below), you can visit [this link](http://127.0.0.1:8000/static/index.html) to view the application on your browser.

### Requirements

Depending on the way of running the application, the following requirements should be installed beforehand:

- docker, docker-compose

or

- Python (>=3.8), pip, pipenv

#### Docker

The application can be easily served using docker, by running the commands below:

```
docker-compose up
```

#### Local Python

There is a bash [script](start.sh) that takes care of the project initialization and local deployment, running the following command:

```
./start.sh
```

### Login instructions

During the initialization process, some sample data of users, movies & votes are being loaded to the application.
You can register as a new user or login as one of the already loaded users using the following credentials:

username: `jane`
password: `Testing-123`

## Documentation

There are more ways to interact with the API other than the provided UI, by either using the Swagger interface or Postman.

### Swagger

While the application is running you can access the Swagger interface that is being served at the [root path](http://127.0.0.1:8000/) of the API.

### Postman

There is a [Postman](https://www.getpostman.com/) [collection](docs/Movierama.postman_collection.json) and [environment](docs/MovieRama.postman_environment.json) that you can use in order to interact with the api or view example responses of it.

## Testing

There is a number of tests written to test the basic functionality and responses of the API. In order to run the tests locally you can execute the following command:

```
pipenv run python manage.py test
```