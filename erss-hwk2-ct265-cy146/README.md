# ECE 568 HTTP Proxy Server

### Members:

* ct265 : Chenglong Tang
* cy146 : Congjia Yu

## Hierarchy of the Project
    .
    ├── dangerlog.txt
    ├── docker-compose.yml
    ├── logs
    │   └── log.txt
    ├── README.md
    ├── src
    │   ├── Dockerfile
    │   ├── proxy
    │   │   ├── deamon
    │   │   ├── helper_function.cpp
    │   │   ├── helper_function.h
    │   │   ├── HttpCache.cpp
    │   │   ├── HttpCache.hpp
    │   │   ├── Http.cpp
    │   │   ├── Http.h
    │   │   ├── launch.cpp
    │   │   ├── logger.cpp
    │   │   ├── logger.h
    │   │   ├── Makefile
    │   │   ├── ProxyException.hpp
    │   │   ├── socket_helper.cpp
    │   │   └── socket_helper.hpp
    │   └── run.sh
    └── Testing.txt

## Command
docker-compose up