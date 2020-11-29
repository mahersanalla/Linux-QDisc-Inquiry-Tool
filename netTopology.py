#!/usr/bin/python
# Benchmark created by Zuher and Maher

from mininet.node import Node
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from mininet.node import CPULimitedHost
from mininet.topo import SingleSwitchTopo
from mininet.util import custom, pmonitor

num_clients = 20

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
	# Attributes
	def build(self, **_opts):
	# Structural members
		self.m_num_of_clients = 0
#		self.m_client_switch = self.addSwitch('s1')
		self.m_server_switch = self.addSwitch('s2')
		self.m_router = self.addHost('router', cls=LinuxRouter, ip='10.0.0.1/24') # ip of router have no importance
		self.m_server = self.addHost(name='server',
   		                        ip='192.168.1.100/24',
    	  		                defaultRoute='via 192.168.1.1')

		self.addLink(self.m_server_switch,
                     self.m_server,
		     		 cls = TCLink)

		self.addLink(self.m_server_switch,
                     self.m_router,
                     intfName2='router-server',
                     params2={'ip': '192.168.1.1/24'},
                     cls = TCLink,
					 bw = 1000)

		for i in range(1, num_clients):
			self.m_num_of_clients += 1
			new_client = self.addHost(name=('client' + str(i + 1)),
				                      ip=('192.168.' + str(i + 1) + '.' +
   									  str(i + 101) + '/24'),
				                      defaultRoute='via 192.168.%d.%d'%(i + 1,i + 1))
			self.addLink(new_client,
                         self.m_router,
                         intfName2='router-client' + str(i + 1),
                         params2={'ip': '192.168.%d.%d/24'%(i + 1, i + 1)},
                         cls = TCLink)
def run():
	topo = NetworkTopo()
	net = Mininet(topo=topo,link=TCLink)
	net.start()
	net['router'].cmd("ifconfig router-server 192.168.1.1/24")
	for i in range(2, num_clients + 1):
		net['router'].cmd("ifconfig router-client%d 192.168.%d.%d/24"%(i, i, i))
	net['server'].cmd("tc qdisc add dev server-eth0 root pfifo_fast")
	net['router'].cmd("tc qdisc add dev router-server root pfifo_fast")
	net['router'].cmd("tc qdisc add dev router-server netem delay 1ms")
#	net['router'].cmd("tc qdisc add dev router-client root pfifo_fast")
	for i in range(2, num_clients+1):
		curr_client='client'+str(i)
		net[curr_client].popen("tc qdisc add dev " + curr_client + "-eth0 root pfifo_fast")

	for i in range(2, num_clients + 1):
		net['server'].popen("iperf3 -s -p " + str(i + 5200) + " &");
		curr_client='client'+str(i) 
		net[curr_client].popen("iperf3 -c 192.168.1.100 -p " + str(i + 5200) + " -t120&")
	CLI(net)
	net.stop()


############################################################################
############################################################################

run()
