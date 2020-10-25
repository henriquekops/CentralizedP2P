# CentralizedP2P
> Python version: 3.8.6

A simple program to run a centralized peer to peer architecture using 
sockets and REST.

## Dependencies
To install all dependencies related to this project, it is recommended 
to create a _virtual environment_ and use the _requirements.txt_ file
present at this repo. To achieve such goal, run:

```
# at CentralizedP2P/

$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## Execution
To execute this program, first you need to start the centralized server
for this P2P architecture. To achieve this, run:

```
# at CentralizedP2P/

$ python src/server.py
```

_**@TODO**: Peer_

## REST routing

To communicate with the centralized server all peers utilize REST calls 
with the same format shown below: 

#### Route: <base_url>/resource
GET: Retrieve peer ips that contains such resource
```
{
    "resource_name": "test.csv"
}
```

POST: Assign a new resource to a peer
```
{
	"peer_id": "42bb7fb8-8f8d-4c1c-b4df-d97c2e78eb7c",
	"peer_ip": "127.0.0.1",
	"resource_name": "test.csv",
	"resource_hash": "12345"
}
```

## Project architecture
The base architecture is shown below:

![image](https://drive.google.com/uc?export=view&id=16Ao56woCVmcw2jlRzOQEhn3UDGAapZXD)