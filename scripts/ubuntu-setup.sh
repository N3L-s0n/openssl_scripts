#!/usr/bin/bash
# This script updates apt packages, then installs git and ansible

apt autoremove -y needrestart

apt update
apt -y upgrade

# installs wget
apt install -y wget

# installs ansible
apt install -y ansible

# install git
apt install -y git
