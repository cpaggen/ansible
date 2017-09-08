This playbook sets up a 3-tier Opencart app on 4 machines (VMs):

- haproxy
- mysql
- web1
- web2

Modify hosts accordingly, and groups_vars/all as those vars are used to configure httpd
Tested and validated with Ubuntu 16.04 and Ubuntu 14.10

You'll notice I am restarting services outside of handlers. I kept running into different
privileges issues between Utopic and Xenial. The service module seems to work well on
both distros.

Note: this script does not provision VMs. My full setup is a pyvmomi script that first
creates VM skeletons and populates a new system in Cobbler. Cobbler then uses a specific
kickstart profile which pulls down common packages, takes care of proxy settings and a few
other minor things. The pyvmomi script is included here.
