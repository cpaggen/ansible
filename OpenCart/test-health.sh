#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m' 
NC='\033[0m'

printf "Running POD tests\n"
for i in {25..45..4}
    do
       echo "Testing haproxy 10.48.58.$i"
       wget --quiet --timeout 3 10.48.58.$i
       if [ -f "index.html" ]
       then
          printf "${GREEN}POD 10.48.58.$i works!\n${NC}"
          rm index.html
       else
	  printf "${RED}POD malfunction!\n${NC}"
       fi
done

for i in {69..84..4}
    do
       echo "Testing haproxy 10.48.58.$i"
       wget --quiet --timeout 3 10.48.58.$i
       if [ -f "index.html" ]
       then
          printf "${GREEN}POD 10.48.58.$i works!\n${NC}"
          rm index.html
       else
	  printf "${RED}POD malfunction!\n${NC}"
       fi
done
