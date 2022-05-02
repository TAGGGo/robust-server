#!/bin/bash
cd proxy
make clean

make

./deamon

while true
do
    sleep 1
done