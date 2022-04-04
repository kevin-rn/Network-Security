#!/bin/bash


while true; do 
	out=$(fail2ban-client status $1 | grep -o "Total banned:.*" | cut -f2)
	(($out >= $2)) && echo $(date +"%Y-%m-%d %H:%M:%S,%3N") && break
done
