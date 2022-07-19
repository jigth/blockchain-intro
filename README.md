# Basic blockchain

A simple blockchain made in Python3, using a the Flask framework, and blockchain concepts.

Based in the: Module 1 - Create a blockchain. Taken and adapted (written by hand) from the following tutorial:

```
Blockchain & Cryptocurrency A-Z Complete Masterclass | Learn How To Build Your First Blockchain
```

## Description

I did it by learning from the tutorial but avoided just copying and made my own implementation, which is similar but has some extra functionalities and differences where I considered it may was a better idea to implement them.

### Used technologies

* Blockchain basic concepts (this code implements Blockchain in a simple way but does not yet implements "descentralization" as P2P networks).

* Python3

* Flask framework

* Virtual environments (python3 -m venv env)

## How to run

* Create a virtual env (recommended for isolation of dependencies)
```
python3 -m venv env
```

* Activate it (if on Windows, execute the "Scripts/activate.bat" file instead of sourcing it)
```
source ./env/bin/activate
```

* Install dependencies
```
pip install -r requirements.txt
```

* Run the project
```
python src/server.py
```

* You're done, you can test the endpoints using an HTTP client such as Postman, Insomnia or cURL if you preffer. The easiest endpoints to test are the following (the other ones are easy but could be a bit confusing at first):
    * "http://127.0.0.1:5000/is-valid"
    * "http://127.0.0.1:5000/mine-block"
    * "http://127.0.0.1:5000/blockchain"
