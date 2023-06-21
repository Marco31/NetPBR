# NetPBR

## For User
Launch NetPBR Application with the following command :

    python3.11 src/App.py

## For Developer

![Réseaux](resources/Network2.png)

Warning : replace XXX.XXX.104.1 -> XXX.XXX.50.1

### Code Analysis

    pyflakes src/*.py
    pylint --disable=C0200,C0301,C0325 src/*.py

### Install dependancies
    python3.11 -m pip install -r requirement.txt

### Diagram
<img src="resources/Diag-Sequence.png"
     alt="Sequence diagram"
     style="float: left; margin-right: 10px;" />

### AI Input

- throughput (bit/s, from Cisco switch)
- pck_loss (%, from Cisco switch)
- latency_avg (from abing)
- latency_sigma (from abing)
- latency_max (from abing)
- Available_Bandwidth : bandwidth (from abing)

## In Development
TODO :
 - [ ] test PBR
 - [ ] fetch list of services use by interface (??)
 - [ ] Waiting function between AI and Controller