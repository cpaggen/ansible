#!/usr/bin/env python
import sys

pod = int(sys.argv[1])
print "Creating files for POD {}".format(pod)

# each pod contains 4 hosts (haproxy, sql, web1, web2)
# the first host of the first pod is 10.48.58.25
# we are creating a simple list of lists as follows:
# ['10.48.58.25', '10.48.58.26', '10.48.58.27', '10.48.58.28']
# ['10.48.58.29', '10.48.58.30', '10.48.58.31', '10.48.58.32']
# ['10.48.58.33', '10.48.58.34', '10.48.58.35', '10.48.58.36']

start_ip="10.48.58.{}"
numOfPods=20
pod_array = []
for i in range(0,numOfPods):
    pod_array.append([])
    for j in range(0, 4):
        lastByte=25 + i*4 + j
        pod_array[i].append(start_ip.format(lastByte))

print pod_array[pod]
hostsFile = '''
[ha-proxy]
%s ansible_user=cisco

[sql]
%s ansible_user=cisco

[web]
%s ansible_user=cisco
%s ansible_user=cisco
''' % tuple(pod_array[pod])

groupVars = '''
---
Web_Server1: "%s"
Web_Server2: "%s"
SQL_Server: "%s"
''' % (pod_array[pod][2], pod_array[pod][3], pod_array[pod][1])

with open('hosts', 'w') as hosts:
    hosts.write(hostsFile)

with open('group_vars/all', 'w') as groupfile:
    groupfile.write(groupVars)
