echo 'Acquire::http::Pipeline-Depth "0";' >> /etc/apt/apt.conf.d/01no-pipeline
systemctl disable iptables-services 

mv /etc/apt/sources.list /home/cisco/
cat <<EOF > /etc/apt/sources.list
deb http://eu.archive.ubuntu.com/ubuntu/ xenial main restricted universe multiverse 
deb-src http://eu.archive.ubuntu.com/ubuntu/ xenial main restricted universe multiverse
deb http://eu.archive.ubuntu.com/ubuntu/ xenial-security main restricted universe multiverse 
deb http://eu.archive.ubuntu.com/ubuntu/ xenial-updates main restricted universe multiverse 
deb http://eu.archive.ubuntu.com/ubuntu/ xenial-proposed main restricted universe multiverse 
deb http://eu.archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse 
deb-src http://eu.archive.ubuntu.com/ubuntu/ xenial-security main restricted universe multiverse 
deb-src http://eu.archive.ubuntu.com/ubuntu/ xenial-updates main restricted universe multiverse 
deb-src http://eu.archive.ubuntu.com/ubuntu/ xenial-proposed main restricted universe multiverse 
deb-src http://eu.archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse 
EOF
wget http://10.48.58.55/KICKSTARTS/ansible-public-key.pub -O /home/cisco/ansible-public-key.pub
mkdir -p /home/cisco/.ssh
cat /home/cisco/ansible-public-key.pub >>  /home/cisco/.ssh/authorized_keys
echo "cisco ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

cat <<EOF > /etc/apt/apt.conf.d/99proxy
Acquire::http::proxy "http://proxy.esl.cisco.com:8080";
Acquire::https::proxy "http://proxy.esl.cisco.com:8080";
EOF

echo "export http_proxy='http://proxy.esl.cisco.com:8080'" >> /home/cisco/.bashrc
echo "export https_proxy='http://proxy.esl.cisco.com:8080'" >> /home/cisco/.bashrc
echo "export no_proxy='localhost,10.48.58.1,10.48.58.2,10.48.58.3,10.48.58.4,10.48.58.5,10.48.58.6,10.48.58.7,10.48.58.8,10.48.58.9,10.48.58.10,10.48.58.11,10.48.58.12,10.48.58.13,10.48.58.14,10.48.58.15,10.48.58.16,10.48.58.17,10.48.58.18,10.48.58.19,10.48.58.20,10.48.58.21,10.48.58.22,10.48.58.23,10.48.58.24,10.48.58.25,10.48.58.26,10.48.58.27,10.48.58.28,10.48.58.29,10.48.58.30,10.48.58.31,10.48.58.32,10.48.58.33,10.48.58.34,10.48.58.35,10.48.58.36,10.48.58.37,10.48.58.38,10.48.58.39,10.48.58.40,10.48.58.41,10.48.58.42,10.48.58.43,10.48.58.44,10.48.58.45,10.48.58.46,10.48.58.47,10.48.58.48,10.48.58.49,10.48.58.50,10.48.58.51,10.48.58.52,10.48.58.53,10.48.58.54,10.48.58.55'" >> /home/cisco/.bashrc


echo "export http_proxy='http://proxy.esl.cisco.com:8080'" >> /etc/environment
echo "export https_proxy='http://proxy.esl.cisco.com:8080'" >> /etc/environment
echo "export no_proxy='localhost,10.48.58.1,10.48.58.2,10.48.58.3,10.48.58.4,10.48.58.5,10.48.58.6,10.48.58.7,10.48.58.8,10.48.58.9,10.48.58.10,10.48.58.11,10.48.58.12,10.48.58.13,10.48.58.14,10.48.58.15,10.48.58.16,10.48.58.17,10.48.58.18,10.48.58.19,10.48.58.20,10.48.58.21,10.48.58.22,10.48.58.23,10.48.58.24,10.48.58.25,10.48.58.26,10.48.58.27,10.48.58.28,10.48.58.29,10.48.58.30,10.48.58.31,10.48.58.32,10.48.58.33,10.48.58.34,10.48.58.35,10.48.58.36,10.48.58.37,10.48.58.38,10.48.58.39,10.48.58.40,10.48.58.41,10.48.58.42,10.48.58.43,10.48.58.44,10.48.58.45,10.48.58.46,10.48.58.47,10.48.58.48,10.48.58.49,10.48.58.50,10.48.58.51,10.48.58.52,10.48.58.53,10.48.58.54,10.48.58.55'" >> /etc/environment


cp /etc/sudoers /home/cisco/
sed -i '/Defaults\tenv_reset/d' /etc/sudoers

timedatectl set-ntp no
export http_proxy="http://proxy.esl.cisco.com:8080"
export no_proxy='localhost,10.48.58.1,10.48.58.2,10.48.58.3,10.48.58.4,10.48.58.5,10.48.58.6,10.48.58.7,10.48.58.8,10.48.58.9,10.48.58.10,10.48.58.11,10.48.58.12,10.48.58.13,10.48.58.14,10.48.58.15,10.48.58.16,10.48.58.17,10.48.58.18,10.48.58.19,10.48.58.20,10.48.58.21,10.48.58.22,10.48.58.23,10.48.58.24,10.48.58.25,10.48.58.26,10.48.58.27,10.48.58.28,10.48.58.29,10.48.58.30,10.48.58.31,10.48.58.32,10.48.58.33,10.48.58.34,10.48.58.35,10.48.58.36,10.48.58.37,10.48.58.38,10.48.58.39,10.48.58.40,10.48.58.41,10.48.58.42,10.48.58.43,10.48.58.44,10.48.58.45,10.48.58.46,10.48.58.47,10.48.58.48,10.48.58.49,10.48.58.50,10.48.58.51,10.48.58.52,10.48.58.53,10.48.58.54,10.48.58.55'

echo 'Acquire::http::Pipeline-Depth "0";' >> /etc/apt/apt.conf.d/01no-pipeline
apt-get update && apt-get install -y apt-transport-https

cat <<EOF > /home/cisco/scripts/proxy-on.sh
export HTTPS_PROXY="http://proxy.esl.cisco.com:8080"
export HTTP_PROXY="http://proxy.esl.cisco.com:8080"
export https_proxy=$HTTPS_PROXY
export http_proxy=$HTTP_PROXY
export no_proxy=`echo 10.48.58.{1..255} | sed 's/ /,/g'`
EOF

cat <<EOF > /home/cisco/scripts/proxy-off.sh
export HTTPS_PROXY=''
export HTTP_PROXY=''
export http_proxy=''
export https_proxy=''
EOF

echo "Ubuntu-plain-setup script done" > /home/cisco/scripts/done.txt
