#!/bin/bash
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

sudo lxc-start host01
sudo lxc-start host02

sleep 5

sudo lxc-attach host01 ip addr add 192.168.12.2/24 dev eth0
sudo lxc-attach host02 ip addr add 192.168.12.3/24 dev eth0

sudo lxc-start host03
