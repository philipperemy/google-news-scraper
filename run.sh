#!/usr/bin/env bash
nohup python3 -u main.py &
sleep 1
tail -f nohup.out
