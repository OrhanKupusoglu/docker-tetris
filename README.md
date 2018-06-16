# Docker-Tetris

This project's aim is to combine [Docker](https://www.docker.com/) and a Web application by [Docker Compose](https://docs.docker.com/compose/). The selected Web applicatication is a beautifully crafted JavaScript game by [ytiurin](https://github.com/ytiurin). The [game](https://github.com/ytiurin/tetris) is a faithful simulation of the original Tetris of 1984.

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
tetris-server/app    0.0.5               5e8a2fc06b2c        14 minutes ago      595MB
tetris-server/base   0.0.5               d2e0fbcc64b8        14 minutes ago      573MB
ubuntu               16.04               5e8b97a2a082        10 days ago         114MB
```

Docker containers can be listed and removed with **docker container** family commands.
For more information check its manual pages.

```
$ man docker-container
$ man docker-container-ls
$ man docker-container-rm

$ docker container ls
$ docker container ls
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                                          NAMES
ec3939e3c083        tetris-server/app:0.0.5   "sh -c /${DIR_PROJEC…"   11 minutes ago      Up 11 minutes       0.0.0.0:8888->8888/tcp, 0.0.0.0:2222->22/tcp   app
```
## Docker Compose

[Docker Compose](https://docs.docker.com/compose/install/) uses [YAML](https://en.wikipedia.org/wiki/YAML) to define and run containers.

Without Docker Compose lengthy **docker build** and **docker run** commands must be issued. Another improvement is using arguments in the Dockerfile scripts. The important [FROM](https://docs.docker.com/engine/reference/builder/#from) instruction can contain references to arguments. See the scripts in the [docker/](./docker) directory.

The [.env](./docker/.venv) file contains variables, all starting with **X_**, which are then used in the [docker-compose.yml](./docker/docker-compose.yml) script.

### Docker Compose Commands

The application can be built and run with a simple shell script, [docker.sh](./docker/docker.sh), which creates a [tarball](https://en.wikipedia.org/wiki/Tarball_(computing)) from the Flask web application. This tarball is referred to in the [Dockerfile-App](./docker/Dockerfile-App) script.

```
$ cd docker
$ ./docker.sh
. . .
WARNING: Image for service app was built because it did not already exist. To rebuild this image you must use `dockerCreating docker_base_1 ... done
Creating app ... done
Creating app ... 
Attaching to app
app     | ++ Flask App: tetris-server/app.py
app     | ++ Flask HTTP port: 8888
app     | ++ started
```

After running the Docker Compose scripts, three images are added. These images can be checked in a new terminal.

The **ubuntu:16:04** is the where **tetris-server/base** is derived from, and in turn the **tetris-server/app** image is derived from this base image. The **tetris-server/base** is prepared with Python 3 projects in mind and can be reached with SSH. Therefore this image might be useful for other Python 3 images, this means that build durations and storage requierements will be less than using directly a Linux distribution.

```
$ docker-compose help

$ docker-compose ps
    Name                   Command               State                       Ports                    
------------------------------------------------------------------------------------------------------
app             sh -c /${DIR_PROJECT}/start.sh   Up       0.0.0.0:2222->22/tcp, 0.0.0.0:8888->8888/tcp
docker_base_1   /bin/bash                        Exit 0                                               
```

The running containers can be stopped with CTRL+C.

```
app     | ++ started
^CGracefully stopping... (press Ctrl+C again to force)
Stopping app ... 
Killing app ... done
```

### Docker Compose Detached Mode

Docker Compose has a **detached mode**:

>  -d Detached mode: Run containers in the background

This is useful to run containers as services.

```
$ docker-compose down
Removing app           ... done
Removing docker_base_1 ... done
Removing network docker_default

$ docker-compose up -d
Creating docker_base_1 ... done
Creating app ... done
Creating app ... 

orhanku@OK-N752VX ~/ME/DEV/docker-tetris/docker $ docker-compose ps
    Name                   Command               State                       Ports                    
------------------------------------------------------------------------------------------------------
app             sh -c /${DIR_PROJECT}/start.sh   Up       0.0.0.0:2222->22/tcp, 0.0.0.0:8888->8888/tcp
docker_base_1   /bin/bash                        Exit 0                                               
```

### Docker Compose Errors

During development of new images with frequent ups and downs, Docker Compose may give errors related to its cache. When this is the case, it is best to remove all project containers (-f for force) and images and rebuild everything.

```
$ docker-compose up
. . .
ERROR: Error: image <IMAGE_NAME/TAG> not found

$ docker ps -a
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                     PORTS                                          NAMES
ec3939e3c083        tetris-server/app:0.0.5    "sh -c /${DIR_PROJEC…"   6 minutes ago       Up 6 minutes               0.0.0.0:8888->8888/tcp, 0.0.0.0:2222->22/tcp   app
dd419b6ad532        tetris-server/base:0.0.5   "/bin/bash"              6 minutes ago       Exited (0) 6 minutes ago                                                  docker_base_1

$ docker container rm -f ec3939e3c083 dd419b6ad532

$ docker image ls
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
tetris-server/app    0.0.5               5e8a2fc06b2c        10 minutes ago      595MB
tetris-server/base   0.0.5               d2e0fbcc64b8        10 minutes ago      573MB
ubuntu               16.04               5e8b97a2a082        10 days ago         114MB

$ docker image rm 5e8a2fc06b2c d2e0fbcc64b8 5e8b97a2a082
```

## SSH

The container can be accessed via SSH on port **2222** by the **root** user with password **1234**.

```
$ ssh root@localhost -p 2222
The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
ECDSA key fingerprint is SHA256:/3EugfEczFa/DHFaUKnLXiBIG/AgYvpzJg1spofJb9c.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[localhost]:2222' (ECDSA) to the list of known hosts.
root@localhost's password: 
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.10.0-38-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@app:~# cd /GAME/
root@app:/GAME# ls -1
requirements.txt
settings.cfg
start.sh
stop.sh
tetris-server
```

Each new built image may trigger a warning. This warning can be eliminated with the suggested **ssh-keygen -f** command.
```
$ ssh root@localhost -p 2222
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:H/lsgpyZSReSu7krJGKvHAwJA3W83cldDrebk6OTav4.
Please contact your system administrator.
Add correct host key in /home/user/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /home/user/.ssh/known_hosts:2
  remove with:
  ssh-keygen -f "/home/user/.ssh/known_hosts" -R [localhost]:2222
ECDSA host key for [localhost]:2222 has changed and you have requested strict checking.
Host key verification failed.

$ ssh-keygen -f "/home/user/.ssh/known_hosts" -R [localhost]:2222

$ ssh root@localhost -p 2222
```

## Game Page

The game page can be reached at [http://localhost:8888/tetris](http://localhost:8888/).

This page is also hosted at [GitHub](https://ytiurin.github.io/tetris/).

## Server Logs

The server logs of a running Tetris container can be checked online at [http://localhost:8888/log](http://localhost:8888/log).

## Favicon

The included [favicon icon](https://en.wikipedia.org/wiki/Favicon.ico) by [Double-J Design](http://www.iconarchive.com/show/origami-colored-pencil-icons-by-double-j-design/green-plus-icon.html) prevents annoying 404-NOT FOUND errors.
