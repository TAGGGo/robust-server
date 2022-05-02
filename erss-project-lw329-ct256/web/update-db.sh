#!/bin/bash

while true
do
    python manage.py makemigrations 
    python manage.py migrate
    python manage.py makemigrations amazon
    python manage.py migrate amazon
    sleep 500 
done
