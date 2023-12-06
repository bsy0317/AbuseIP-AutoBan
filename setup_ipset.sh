#!/bin/bash

yum install -y ipset
#ipset create blockip iphash
ipset create blockip hash:ip hashsize 4096 maxelem 1000000
iptables -I INPUT 1 -m set --match-set blockip src -j DROP