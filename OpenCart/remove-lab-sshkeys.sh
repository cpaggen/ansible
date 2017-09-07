#!/bin/bash
for i in {25..50}; do
            ssh-keygen -f "/root/.ssh/known_hosts" -R 10.48.58.$i
done

