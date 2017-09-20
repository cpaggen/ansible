#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m' 
NC='\033[0m'

printf "Running POD tests\n"

test_pod()
{
for ((i = $1; i <= $2; i+=4))
    do
       echo "Testing haproxy 10.48.58.$i"
       wget --quiet --timeout 3 10.48.58.$i
       db=$(($i+1))
       maria=`nc 10.48.58.$db 3306 -w 1`
       if [[ $maria == *"MariaDB"* ]]
       then
          printf "${GREEN}DB is up!\n${NC}"
       else
          printf "${RED}DB is down!\n${NC}"
       fi
       if [ -f "index.html" ]
       then
          printf "${GREEN}Haproxy 10.48.58.$i works!\n${NC}"
          rm index.html
       else
	  printf "${RED}POD malfunction!\n${NC}"
       fi
done
}

test_pod 25 45
test_pod 69 84

