#!/bin/bash
sudo apt update
sudo apt install lxc bridge-utils net-tools lxc-templates -y
sudo brctl addbr br0
sudo brctl addbr br1
sudo ifconfig br0 up
sudo ifconfig br1 up
sudo ip link add veth0 type veth peer name veth1
sudo ifconfig veth0 up
sudo ifconfig veth1 up
sudo brctl stp br0 on
sudo brctl stp br1 on
sudo brctl addif br0 veth0
sudo brctl addif br1 veth1

sudo lxc-create -t ubuntu -n host01
sudo lxc-create -t ubuntu -n host02
sudo sed -i 's/lxc.net.0.link = lxcbr0/lxc.net.0.link = br0/g' /var/lib/lxc/host01/config
sudo sed -i 's/lxc.net.0.link = lxcbr0/lxc.net.0.link = br1/g' /var/lib/lxc/host02/config
sudo lxc-start host01
sudo lxc-start host02

sleep 5

sudo lxc-attach host01 ip addr add 192.168.12.2/24 dev eth0
sudo lxc-attach host02 ip addr add 192.168.12.3/24 dev eth0

sudo lxc-create -t ubuntu -n host03
echo "
lxc.net.1.type = veth
lxc.net.1.link = br0
lxc.net.1.flags = up
lxc.net.1.hwaddr = 00:16:3e:c3:de:ad

lxc.net.2.type = veth
lxc.net.2.link = br1
lxc.net.2.flags = up
lxc.net.2.hwaddr = 00:16:3e:c3:be:ef" | sudo tee -a /var/lib/lxc/host03/config
sudo lxc-start host03

sleep 5

sudo lxc-attach -n host03 -- apt update
sudo lxc-attach -n host03 -- apt install -y python3-pip tcpdump bridge-utils
