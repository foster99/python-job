# DevServer machine for Docker Infraestructure

You'll need to have Vagrant and ansible installed in the host machine

Features
--------
- IP: 192.168.70.70

Installation
------------

- Install Vagrant:

    [vagrant downloads page](https://www.vagrantup.com/downloads.html)

Instructions
------------

**[1]** Create the code folder inside code project's home folder (named CodeProjects in this case):

```
$ mkdir -p CodeProjects/code
```

**[2]** Inside the CodeProjects folder clone/copy the vagrant project in a folder called server

```
$ cd CodeProjects
$ git clone git@bitbucket.org:########.git server
```

**[3]** Inside, run vagrant

```
$ cd server
$ vagrant up
```
This will:

- Install git

- Install docker

- Install Containers

- Install commands

**[4]** Once Vagrant is up, connect with vagrant using vagrant ssh and change to root user using (inside vagrant):
```
$ sudo su - \\ (password: vagrant)
```

**[5]** Now, if you have finished the installation, with all the code installed, then you can create the containers:


Hosts (your hosts table must be like this)
-------------------

```
192.168.70.70   sfexam.delectame.develop
```

Available Commands
-------------------

- `dm-docker-up [container]`: equal to docker-compose up (all containers or just one)

- `dm-docker-rebuild [container]`: Stop and recreate an **image** and a container.

- `dm-docker-logs`: Shows docker-compose logs

- `dm-docker-ps`: shows all instance status (same as docker-compose ps)

- `dm-docker-down [container]`: shuts down a docker images

Available Containers
-------------------

- `sfexam`: Symfony4 Container

```
xDebug is enabled for remote debugging on port 9006
```

- `mariadb`: MariaDB 10.4.12 Container 

```
`user`: root 
`pwd`: delectaRoot1234! 
```

- `mongodb`: MongoDB 4.2.7 Container

```
`user`: delecta_root 
`pwd`: delectaRoot1234!
```