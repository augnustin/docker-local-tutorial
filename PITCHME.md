# Use Docker for your local environment

Workshop by [Augustin Riedinger](https://augustin-riedinger.fr)
(![Twitter](images/twitter.png): [@augnustin](https://twitter.com/Augnustin))

At [Capitole du Libre](https://2017.capitoledulibre.org) 19th November 2017

---

### Prerequisite

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

### Motivations

Are you working on a single code base **for your entire life**?

If so, you are free to go. :-)

Most of the time, you will work on `project X` which requires Ruby 2+, Rails 5.1, Node 8+ and PostgreSQL 8.1 along with `project Y` which doesn't work without Node 10 and PostgreSQL 9.3 and sometimes get back on your 3.2 Ruby-on-Rails `Z project`.

![Technology dependencies struggle](images/confused.jpg)

### Solutions

#### RVM, NVM, GVM tools?

- add complexities
- doesn't exist for every technology (eg. Postgres, Mongo)
- local environment takes longer to setup
- messes your machine

#### Virtualbox, Vagrant?

- heavy in resources **AND** memory

Now we have **DOCKER**!!

---

### What is Docker?

You've probably heard of it. It's fashion now!

