#!/bin/bash

sleep 30
cd ~/bear-o-meter

while true
do
	/home/pi/.virtualenvs/bear/bin/python my_test.py
	sleep 5
done
