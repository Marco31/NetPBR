# NetPBR

Hello to you young entrepreneur,

Did you know that 95% of the population misuse internet network,

so you want to be part of it ? You have to ask the rights questions.

## For User
### Install dependancies
- You have to compile abing (https://github.com/RichardWithnell/abing) and move binaries to /src/libs
```sh
python3.11 -m pip install -r requirement.txt
```

### Use
- Launch NetPBR Application with the following command :

```sh
python3.11 src/App.py
```

## For Developer

![Réseaux](resources/Network2.png)

Warning : All theses IP are private IP so you need to set IP in setting of the application according to your network

### Code Analysis

    pyflakes src/*.py
    pylint --disable=C0200,C0301,C0325 src/*.py


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