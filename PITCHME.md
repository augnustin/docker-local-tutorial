# Use Docker for your local environment

Workshop by [Augustin Riedinger](https://augustin-riedinger.fr)
(![Twitter](pitchme/images/twitter.png): [@augnustin](https://twitter.com/Augnustin))

At [Capitole du Libre](https://2017.capitoledulibre.org) 19th November 2017

---

## Prerequisite

To attend this workshop, you need to have the following installed:

- [Docker](https://docs.docker.com/engine/installation/)
- [Docker-compose](https://github.com/docker/compose/releases)
- Aliases (we'll detail them later):

```
alias docker-enter="docker-compose run --rm --service-ports app /bin/bash"
alias docker-enter-again="docker-compose run --rm app /bin/bash"
alias docker-clean="docker ps -a | grep 'Exited\|Created' | cut -d ' ' -f 1 | xargs docker rm"
```

---

## Motivations

Are you working on a single code base **for your entire life**?

If so, you are **free to go**. :-)

Most of the time, you will work on `project X` which requires Ruby 2+, Rails 5.1, Node 8+ and PostgreSQL 8.1 along with `project Y` which doesn't work without Node 10 and PostgreSQL 9.3 and sometimes get back on your 3.2 Ruby-on-Rails `Z project`.

---

## Solutions

#### RVM, NVM, GVM tools?

- adds complexities
- doesn't exist for every technology (eg. Postgres, Mongo)
- local environment takes longer to setup
- messes your machine

#### Virtualbox, Vagrant?

- heavy in resources **AND** memory

Now we have **DOCKER**!!

---

## What is Docker?

You've probably heard of it. It's fashion now!

![Docker vs VM](pitchme/images/docker-vs-vm.png)

To keep it simple:

+ reuses the OS core functionnalities
+ but isolates from other applications

---

## Step 1: Let's start an app

Let's make a simple Python [Flask](http://flask.pocoo.org) Hello World app.

Why? Simply because python is popular and easy to read. But this tutorial could work with **any unix-compliant technology**.

How would you do that without docker?

---

### With Docker, 2 extra files

- `Dockerfile`

```
FROM ubuntu:latest
```

- `docker-compose.yml`

```
app:
  build: .
  volumes:
    - .:/app
  ports:
    - "5000:5000"
```

Now type `docker-enter`...

---

### Inside the Matrix

![You are inside](pitchme/images/docker-matrix.jpg)

What do you want to do?

- `whoami`
- `pwd`
- `ls`
- `cd app`
- `ping gnu.io`
- etc.

---

### Back to our app

Flask's [getting started](http://flask.pocoo.org) says to create `hello.py`:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello Capitole du Libre!"

app.run(host='0.0.0.0')
```

And in the terminal we need to install [`pip`](https://www.rosehosting.com/blog/how-to-install-pip-on-ubuntu-16-04/) then `Flask`:

```
apt-get update && apt-get install -y python-pip # no need sudo, we are root :)
pip install Flask
FLASK_APP=hello.py flask run
```

Go check [http://localhost:5000](http://localhost:5000) ;-)

---

### How it works?

Let's have a deeper look at `docker-compose.yml`:

```
build: . # When doing `docker-compose build`, uses the `Dockerfile` in working directory
volumes:
  - .:/app # Shares your machine working directory with docker's `/app`
ports:
  - "5000:5000" # Shares your machine 5000 port with docker's 5000
```

And `Dockerfile`:

```
FROM python:latest
```

And `docker-enter` = `docker-compose run --rm --service-ports app /bin/bash`

---

### Saving changes

If I `exit` docker, and then `docker-enter` again to restart my server, I get:

```
root@d774482d9d98:/# FLASK_APP=hello.py flask run
bash: flask: command not found
```

That's because docker saves thing only during the `build` operation. All the rest is disposable.

To achieve this, edit your `Dockerfile`

```
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip
RUN pip install Flask
RUN cd /app
```

And run `docker-compose build`. Now you can retry `docker-enter`.

---

### `docker-compose.yml` pimped

`docker-compose` is a utility to store `docker` parameters in a separated file: `docker-compose.yml`.

Eg. The above command docker equivalent would be

`docker run -it -p 5000:5000 -v /home/augustin/Workspace/docker-local-tutorial/tutorial:/app ubuntu:latest bash`

There are many possible entries in a `docker-compose.yml` file. Now let's add the most interesting: `command`:

```
app:
  build: .
  command: flask run
  volumes:
    - .:/app
  ports:
    - "5000:5000"
  environment:
    FLASK_APP: hello.py
```

And now type `docker-compose up`. :-)

## Persistent database

Now you'll want to have a database system connected, right?

How do you do?

[Install Redis in your container](https://www.google.com/search?q=install+redis+ubuntu) ??

### The Docker way

1. One container per dependency never more
2. Use DockerHub, the Github of Docker Images

### New `docker-compose.yml`

```
app:
  build: .
  command: flask run
  volumes:
    - .:/app
  working_dir: /app
  ports:
    - "5000:5000"
  environment:
    FLASK_APP: hello.py
  links:
    - db
db:
  image: redis
```

And `docker-enter`...

### Where is my DB??

Your container is linked to a DB one. How do you know? Environment variables!

```
root@6bceb2f600f6:/app# printenv
STEP3_DB_1_PORT_6379_TCP_PROTO=tcp
HOSTNAME=6bceb2f600f6
DB_NAME=/step3_app_run_1/db
DB_PORT_6379_TCP_PORT=6379
TERM=xterm
DB_PORT=tcp://172.17.0.3:6379
...
DB_1_PORT_6379_TCP=tcp://172.17.0.3:6379
DB_1_ENV_GOSU_VERSION=1.10
_=/usr/bin/printenv
```

### Use it!

```
app.config.update(
  # DB_1_PORT_6379_TCP=tcp://172.17.0.3:6379
  REDIS_URL=os.environ['DB_1_PORT_6379_TCP'].replace('tcp://', 'redis://')
)
```

