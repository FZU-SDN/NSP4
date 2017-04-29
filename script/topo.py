#!/usr/bin/env python

# Copyright 2017 FuZhou University SDNLab, Edu. 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController, RemoteController

from p4ovs_mininet import P4Switch

import argparse
from time import sleep
import os
import subprocess

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')

parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
parser.add_argument('--controller-ip', help='Controller IP Address',
                    type=str, action="store", required=False)
parser.add_argument('--controller-port', help='Controller Port',
                    type=int, action="store", required=False)

args = parser.parse_args()

# Use to config the hosts
hosts = []

class MyTopo(Topo):
    def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        for i in xrange(nb_switches):
            thrift_port = _THRIFT_BASE_PORT+i
            self.addSwitch('s%d' % (i + 1), # dpid  = str('0x'+i), # add dpid
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = thrift_port,
                            pcap_dump = True,
                            device_id = i)
        
        for h in xrange(nb_hosts):
            hi = self.addHost('h%d' % (h + 1))
            hosts.append(hi)

def Connect(net, links):
    # Connect the elements on the DataPlane.
    for i, j in links:
        print i, j
        a = net.get(i)
        b = net.get(j)
        net.addLink(a, b)

def HostConfig(net, nb_hosts):
    # Config the hosts by IP and MAC address
    for i in xrange(nb_hosts):
        print 'Config hosts h%d' % (i+1)
        obj = net.get(hosts[i])
        obj.setIP("10.0.0.%d" % (i+1))
        obj.setMAC("00:00:00:00:00:0%d" % (i+1))

def read_topo():
    nb_hosts = 0
    nb_switches = 0
    links = []
    with open("topo.txt", "r") as f:
        line = f.readline()[:-1]
        w, nb_switches = line.split()
        assert(w == "switches")
        line = f.readline()[:-1]
        w, nb_hosts = line.split()
        assert(w == "hosts")
        for line in f:
            if not f: break
            a, b = line.split()
            links.append( (a, b) )
    return int(nb_hosts), int(nb_switches), links

def main():
    nb_hosts, nb_switches, links = read_topo()
    
    mode = args.mode

    topo = MyTopo(args.behavioral_exe,
                  args.json,
                  nb_hosts, nb_switches, links)

    net = Mininet(topo = topo,
                  switch = P4Switch,
                  controller = RemoteController)
                  # controller = OVSController)
    
    # [Option] TODO: Add your own SDN Controller using net.addController()
    # controller_IP = args.controller_ip
    # controller_port = args.controller_port
    # net.addController('c0', controller=RemoteController, ip=controller_IP, 
    #                   port=controller_port)
    
    Connect(net, links)
    HostConfig(net, nb_hosts)
    
    net.start()

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
        
	for off in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload eth0 %s off" % off
            print cmd
            h.cmd(cmd)
        
	print "disable ipv6"
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
        h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
	
	if mode == "l2":
            h.setDefaultRoute("dev eth0")
        else:
            h.setARP(sw_addr[n], sw_mac[n])
	    h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
	#h.describe()

    sleep(1)

    print "Ready !"

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
