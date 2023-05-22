# images_api
Api for managing images. Made for a test task.
<br/>
PS: no async here(considering that it will be launched in aws lambda)

## Overview
`Type`: Backend, REST api <br/>
`Technologies`: FastAPI, Pymongo, Docker <br/>

## Running via docker-compose
```bash
$ docker-compose up -d
```

## Installing on a local machine
This project requires python 3.10. Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools)

Install requirements:

```bash
$ pip install --upgrade pip pip-tools
$ make
```

Run the server:

```bash
$ export MONGODB_URL=<your_mongodb_url>
$ cd src
$ uvicorn main:app --reload
```

Testing:

PS: preferable if you have a running instance of mongodb(locally or via Docker)
```bash
# run lint
$ make linting

# run unit tests
$ make test
```

Development servers:

```bash
# run django dev server
$ ./manage.py runserver

```