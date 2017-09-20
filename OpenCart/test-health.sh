#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m' 
NC='\033[0m'

rm index.html
printf "Running POD tests\n"

test_pod()
{
for ((i = $1; i <= $2; i+=4))
    do
       haproxy=10.48.58.$i
       db=10.48.58.$(($i+1))
       web1=10.48.58.$(($i+2))
       web2=10.48.58.$(($i+3))
       wget --quiet --timeout 3 $haproxy && printf "${GREEN}Haproxy $haproxy works!\n${NC}" || printf "${RED}POD malfunction!\n${NC}"
       wget --quiet $web1 --timeout 3 && printf "web1 $web1 up\n" || printf "${RED}web1 $web1 down${NC}\n"
       wget --quiet $web2 --timeout 3 && printf "web2 $web2 up\n" || printf "${RED}web2 $web2 down${NC}\n"
       rm index.html.*
       maria=`nc $db 3306 -w 1`
       if [[ $maria == *"MariaDB"* ]]
       then
          printf "${GREEN}DB $db is up!\n${NC}"
       else
          printf "${RED}DB $db is down!\n${NC}"
       fi
       printf "========\n"
done
}

test_pod 25 45
test_pod 69 84

