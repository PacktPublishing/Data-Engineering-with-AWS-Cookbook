#!/bin/bash
## Name: SSM Agent Installer Script
## Description: Installs SSM Agent on EMR cluster EC2 instances and update hosts file
##
sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
sudo status amazon-ssm-agent >>/tmp/ssm-status.log
## Update hosts file
echo "\n ########### localhost mapping check ########### \n" > /tmp/localhost.log
lhost=`sudo cat /etc/hosts | grep localhost | grep '127.0.0.1' | grep -v '^#'`
v_ipaddr=`hostname --ip-address`
lhostmapping=`sudo cat /etc/hosts | grep $v_ipaddr | grep -v '^#'`
if [ -z "${lhostmapping}" ];
then
echo "\n ########### IP address to localhost mapping NOT defined in hosts files. add now ########### \n " >> /tmp/localhost.log
sudo echo "${v_ipaddr} localhost" >>/etc/hosts
else
echo "\n IP address to localhost mapping already defined in hosts file \n" >> /tmp/localhost.log
fi
echo "\n ########### IP Address to localhost mapping check complete and below is the content ########### " >> /tmp/localhost.log
sudo cat /etc/hosts >> /tmp/localhost.log

echo "\n ########### Exit script ########### " >> /tmp/localhost.log
