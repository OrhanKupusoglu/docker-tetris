# Docker-Tetris

This project's aim is to combine [Docker](https://www.docker.com/) and a Web application by [Docker Compose](https://docs.docker.com/compose/). The selected Web applicatication is a beautifully crafted JavaScript game by [ytiurin](https://github.com/ytiurin). The [game](https://github.com/ytiurin/tetris) is a faithful simuation of the original Tetris of 1984.

Although to host this game consisting of only static pages [Flask](http://flask.pocoo.org/) is an overkill, the main idea of using Docker containers might be useful for a real Flask application.

## Docker

Docker is a [containerization](https://docs.docker.com/get-started/) tool. The free [Community Edition](https://www.docker.com/community-edition) is easy to [install](https://docs.docker.com/install/). The optional [post-installation steps](https://docs.docker.com/install/linux/linux-postinstall/) enable running Docker commands without root privileges.

```
$ sudo groupadd docker

$ sudo usermod -aG docker $USER
```
Logout-login is required.


### Docker Commands

Docker images can be listed and removed with **docker image** family commands.
For more information check its manual pages.

```
$ man docker-image
$ man docker-image-ls
$ man docker-image-rm

$ docker image ls
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
tetris-server/app    0.0.1               5d8d8c3b6bdc        40 seconds ago      591MB
tetris-server/base   0.0.1               c072bf4c7b56        50 seconds ago      570MB
ubuntu               16.04               0458a4468cbc        4 weeks ago         112MB
```

Docker containers can be listed and removed with **docker container** family commands.
For more information check its manual pages.

```
$ man docker-container
$ man docker-container-ls
$ man docker-container-rm

$ docker container ls
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                          NAMES
ad3029cb89a0        tetris-server/app:0.0.1   "sh -c /${DIR_PROJEC…"   3 minutes ago       Up 3 minutes        0.0.0.0:8888->8888/tcp, 0.0.0.0:2222->22/tcp   app

```
## Docker Compose

Docker Compose uses [YAML](https://en.wikipedia.org/wiki/YAML) to define and run containers.

Without Docker Compose lengthy **docker build** and **docker run** commands must be issued. Another improvement is using arguments in the Dockerfile scripts. The important [FROM](https://docs.docker.com/engine/reference/builder/#from) instruction can contain references to arguments. See the scripts in the [docker/](./docker) directory.

The [.env](./docker/.venv) file contains variables, all starting with **X_**, which are then used in the [docker-compose.yml](./docker/docker-compose.yml) script.

### Docker Compose Commands

The application can be built and run with a simple shell script, [docker.sh](./docker/docker.sh), which creates a [tarball](https://en.wikipedia.org/wiki/Tarball_(computing)) from the Flask web application. This tarball is refered to in the [Dockerfile-App](./docker/Dockerfile-App) script.

```
$ cd docker
$ ./docker.sh
```

After running the Docker Compose scripts, three images are listed. The **ubuntu:16:04** is the where **tetris-server/base:0.0.1** is derived from, and in turn the **tetris-server/app:0.0.1** mage is derived from this base image. The **tetris-server/base:0.0.1** is prepared with Python 3 projects in mind and can be reached with SSH. Therefore this image might be useful for other Python 3 images, this means that build durations and storage requierements will be less than using directly a well-known Linux distribution.

```
$ docker-compose help

$ docker-compose ps
    Name                   Command               State                       Ports
------------------------------------------------------------------------------------------------------
app             sh -c /${DIR_PROJECT}/start.sh   Up       0.0.0.0:2222->22/tcp, 0.0.0.0:8888->8888/tcp
docker_base_1   /bin/bash                        Exit 0
```

Docker Compose may give errors related to its cache. When this is the case, it is best to remove all project containers (-f for force) and images and rebuild everything.
```
$ docker-compose up
. . .
ERROR: Error: image <IMAGE_NAME/TAG> not found

$ docker container ls
$ docker container rm -f ad3029cb89a0

$ docker image ls
$ docker image rm 5d8d8c3b6bdc c072bf4c7b56

$ docker-compose down
$ docker-compose rm
```

## Server Logs

The server logs of a running Tetris container can be checked online at [/log](localhost:8888/log).

## Favicon

The included [favicon icon](https://en.wikipedia.org/wiki/Favicon.ico) by [Double-J Design](http://www.iconarchive.com/show/origami-colored-pencil-icons-by-double-j-design/green-plus-icon.html) prevents annoying 404-NOT FOUND errors.
