# CentralizedP2P
> Python version: 3.8.6

A simple program to run a centralized peer-to-peer architecture using 
sockets and HTTP REST.

## Dependencies

It is recommended to use [pyenv](https://github.com/pyenv/pyenv) for 
managing your python versions.

To install all dependencies related to this project, it is recommended 
to create a _virtual environment_ and use the _requirements.txt_ file
present at this repo. To achieve such goal, run:

```
# at CentralizedP2P/

# virtual environment
$ python -m venv venv
$ . venv/bin/activate

# install
$ pip install -r requirements.txt
```

## Execution
To execute this program, first you need to start the centralized server
for this P2P architecture. To achieve this, run:

```
# at CentralizedP2P/

$ python src/server.py
```

Then you can start peers to communicate with the centralized server and
between each other. To achieve this, run:
```
# at CentralizedP2P/

$ python src/server.py <peer_ip:ipv4> <server_ip:ipv4> <action_port:int> <listen_port:int>
```

> Field 'action_port' refers to the port that is used by peer's CLI 
(main thread).

> Field 'listen_port' refers to the port that listens to socket requests 
(runs in a separated thread).

## REST routing

To communicate with the centralized server all peers utilize REST calls 
with the same format, shown below: 

#### /resource
GET: Retrieve every peer's info registered at database.

```
# request body
{}
``` 

GET: Retrieve peer's info that contains such resource.
```
# request body
{
    "resource_name": "test.csv"
}
```

POST: Assign a new resource to a peer.
```
# request body
{
	"peer_id": "42bb7fb8-8f8d-4c1c-b4df-d97c2e78eb7c",
	"peer_ip": "127.0.0.1",
	"peer_port": 3000,
	"resource_name": "test.csv",
	"resource_path": "./tests",
	"resource_hash": "dea311be2ca928ae1d6ba5ab28b53c60"
}
```

#### /heartbeat
POST: Tell server that peer still alive.
```
{
    "peer_id": "42bb7fb8-8f8d-4c1c-b4df-d97c2e78eb7c"
}
```

## Project architecture
The base architecture is shown below:

![image](https://drive.google.com/uc?export=view&id=16nh2_rswtXP-l3v3l1vy2A7Hr-1iQ-6Q)
