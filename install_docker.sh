#!/bin/bash


sudo yum update -y

sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install -y docker-ce docker-ce-cli containerd.io

sudo systemctl start docker

sudo systemctl enable docker

sudo usermod -aG docker ec2-user

sudo docker run hello-world

echo "run the following commands:" 
echo "sudo passwd ec2-user"
echo "su - ec2-user"
echo "docker run -p 27777:27017 --privileged -it mongodb/atlas bash"

