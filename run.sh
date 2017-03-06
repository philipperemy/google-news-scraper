#!/usr/bin/env bash
nohup python3 -u main_no_vpn.py &
sleep 1
tail -f nohup.out
