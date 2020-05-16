# SnowGlobe
A python package to manage docker development environments


## Installation
Prerequisite
 - Requires python version 3.6 or higher
 - Requires docker CLI setup on host machine

Installation
```
$ pip install snowglobe
```

## Usage
> List of all commands

Command:
```
$ snowglobe -h
usage: snowglobe [-h] {list,inspect,setup,remove,reset,start,exec,stop} ...

positional arguments:
  {list,inspect,setup,remove,reset,start,exec,stop}
                        Sub commands for snowglobe
    list                Get list configured environments
    inspect             Inspect a configured environment
    setup               Setup a new environment
    remove              Remove an existing environment
    reset               Reset an existing environment
    start               Start an existing environment
    exec                Exec commands on an existing environment
    stop                Stop an existing environment

optional arguments:
  -h, --help            show this help message and exit
```

## List existing environments
> This command will list all existing environments setup through snowglobe.
By default this will show the demo environment which can be used for reference. 

Command:
```
$ snowglobe list
```

Example
```
$ snowglobe list
Environments:
webapp
```
---
## Get template config
> This command will print a template with placeholder config.

Command:
```
$ snowglobe template
```

Example:
```
$ snowglobe template > webapp.json
$ cat webapp.json
{
    "image": "IMAGE:TAG",
    "name": "NAME",
    "create": {
        "command": [],
        "entrypoint": "ENTRYPOINT",
        "envs": {
            "KEY": "VALUE"
        },
        "ports": [
            {
                "containerPort": 8080,
                "hostPort": 8080
            }
        ],
        "volumes": [
            {
                "hostPath": "/PATH/ON/HOST",
                "containerPath": "/PATH/ON/CONTAINER",
                "mode": "rw"
            }
        ],
        "options": "-it --hostname HOSTNAME"
    },
    "start": "",
    "execs": [
        {
            "name": "EXEC-NAME",
            "command": "EXEC_COMMAND",
            "options": "-it"
        }
    ]
}
```
---
## Setup an environment
> This command will setup a new docker environment on snowglobe

Command:
```
$ snowglobe setup <environment_name> -f <config_file>
```

Example:
> In this example we will setup an nginx dev environment called webapp. You can use the template command to help create 
this nginx environment. Create a file webapp.json and enter the following config in it. Note that we are not using any 
shared volumes in this example. 
```
{
    "image": "nginx:latest",
    "name": "webapp",
    "create": {
        "command": [],
        "entrypoint": "",
        "envs": {
            "SERVER": "webapp"
        },
        "ports": [
            {
                "containerPort": 80,
                "hostPort": 8080
            }
        ],
        "volumes": [],
        "options": "-it --hostname webapp"
    },
    "start": "",
    "execs": [
        {
            "name": "shell",
            "command": "bash",
            "options": "-it"
        },
        {
            "name": "echo",
            "command": "echo Hello World",
            "options": "-it"
        },
    ]
}
```
```
$ snowglobe setup webapp -f webapp.json
Setting up environment: webapp
Creating environment: webapp
6f36c69ef2499aed0c24b3d5dbbbce05443b7e5e8eef508fa01c5764a24e9f15
```
## Inspect an environment
> This command will print the configuration of an environment in json format

Command:
```
$ snowglobe inspect <environment_name>
```

Example: 
```
$ snowglobe inspect webapp
{
    "image": "nginx:latest",
    "name": "webapp",
    "create": {
        "command": [],
        "entrypoint": "",
        "envs": {
            "SERVER": "webapp"
        },
        "ports": [
            {
                "containerPort": 80,
                "hostPort": 8080
            }
        ],
        "volumes": [],
        "options": "-it --hostname webapp"
    },
    "start": "",
    "execs": [
        {
            "name": "shell",
            "command": "bash",
            "options": "-it"
        },
        {
            "name": "echo",
            "command": "echo Hello World",
            "options": "-it"
        },
    ]
}
```
---
## Start an environment
> This command will start the environment. The start options in the config will be used while starting the container.

Command:
```
$ snowglobe start <environment_name>
```

Example:
```
$ snowglobe start webapp
Starting environment: webapp
webapp
```
---
## Exec a command in an environment
> This command will execute a profile in the environment. The environment must be already started before running this 
command. It takes in the name of the execution profile.

Command:
```
$ snowglobe exec <environment_name> <exec_name>
```

Example:
```
$ snowglobe exec webapp echo
Executing environment: webapp. Exec name: echo
'Hello World'

$ snowglobe exec webapp shell
Executing environment: webapp. Exec name: shell
root@webapp:/#
```
---
## Stop an environment
> This command will stop a running environment.

Command:
```
$ snowglobe stop <environment_name>
```

Example:
```
$ snowglobe stop webapp
Stopping environment: webapp
webapp
```
---
## Reset an environment
> This command will reset an existing environment. This will recreate the container.

Command:
```
$ snowglobe reset <environment_name>
```

Example:
```
$ snowglobe reset webapp
Resetting environment: webapp
Stopping environment: webapp
webapp
Deleting environment: webapp
webapp
Creating environment: webapp
c848f87b99c4e301d1debe05d166fa06d7b097d10524b7a74a689385c3f89adf
```
---
## Remove an environment
> This command will remove an environment.

Command:
```
$ snowglobe remove <environment_name>
```

Example:
```
$ snowglobe remove webapp
Deleting up environment: webapp
Stopping environment: webapp
webapp
Deleting environment: webapp
webapp
```
