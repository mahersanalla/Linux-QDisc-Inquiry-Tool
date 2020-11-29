#!/usr/bin/python

from mininet.node import Node
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

# d1 <--> s1 <--> r <--> s2 <--> d2
# tc qdisc add dev d1-eth0 root pfifo_fast
def createHost(Topo,host_name,host_ip,gw,m_router,m_interface,host_number):
	s = Topo.addSwitch('s'+str(host_number));
	Topo.addLink(s,
		     m_router,
		     intfName2=m_interface,
		     params2={'ip': host_ip+'/24'},
		     cls=TCLink)
	h = Topo.addHost(name=host_name,
			ip=host_ip,
			defaultRoute=gw)
	Topo.addLink(h,s,cls = TCLink); 
	#net[r].cmd("ifconfigs"+str(host_number)+"-router "+host_ip+"/24")
	return h;


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r = self.addHost('r', cls=LinuxRouter, ip='10.0.0.1/24')

        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add host-switch links in the same subnet
        self.addLink(s1,
                     r,
                     intfName2='s1-router',
                     params2={'ip': '192.101.0.100/24'},
		     cls = TCLink)

        self.addLink(s2,
                     r,
                     intfName2='s2-router',
                     params2={'ip': '192.102.0.100/24'},
                     cls = TCLink)
 
        self.addLink(s3,
                     r,
                     intfName2='s3-router',
                     params2={'ip': '192.103.0.100/24'},
                     cls = TCLink)
     
        # Adding hosts specifying the default route
        server1 = self.addHost(name='server1',
                          ip='192.101.0.101/24',
                          defaultRoute='via 192.101.0.100')
        h2 = self.addHost(name='h2',
                          ip='192.102.0.102/24' ,
                          defaultRoute='via 192.102.0.100')
        h3 = self.addHost(name='h3',
                          ip='192.103.0.103/24',
                          defaultRoute='via 192.103.0.100')

        # Add host-switch links
        self.addLink(server1, s1, cls = TCLink)
        self.addLink(h2, s2, cls = TCLink)
        self.addLink(h3, s3, cls = TCLink)
	createHost(self,'h4','192.104.0.104','192.104.0.100',r,'s4-router',4);
	createHost(self,'h5','192.105.0.105','192.105.0.100',r,'s5-router',5);
	createHost(self,'h6','192.106.0.106','192.106.0.100',r,'s6-router',6);
	createHost(self,'h7','192.107.0.107','192.107.0.100',r,'s7-router',7);
	createHost(self,'h8','192.108.0.108','192.108.0.100',r,'s8-router',8);

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo,link=TCLink)
    net.start()

    # Add routing for reaching networks that aren't directly connected
    # info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth2"))
    # info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth2"))
    net['r'].cmd("ifconfig s1-router 192.101.0.100/24")   
    net['r'].cmd("ifconfig s2-router 192.102.0.100/24") 
    net['r'].cmd("ifconfig s3-router 192.103.0.100/24") 
    net['r'].cmd("ifconfig s4-router 192.104.0.100/24") 
    net['r'].cmd("ifconfig s5-router 192.105.0.100/24") 
    net['r'].cmd("ifconfig s6-router 192.106.0.100/24") 
    net['r'].cmd("ifconfig s7-router 192.107.0.100/24") 
    net['r'].cmd("ifconfig s8-router 192.108.0.100/24") 
    net['server1'].cmd("tc qdisc add dev server1-q root pfifo_fast")
    net['r'].cmd("tc qdisc add dev r-h2 root pfifo_fast")
#    net['server1'].cmd("route add default gw 192.101.0.100")

    #net['server1'].cmd("iperf3 -s")
   # net['h2'].cmd("iperf3 -c 192.101.0.101 -t120")
  #  net['h3'].cmd("iperf3 -c 192.101.0.101 -t120")
 #   net['h4'].cmd("iperf3 -c 192.101.0.101 -t120")
#    net['h5'].cmd("iperf3 -c 192.101.0.101 -t120")
    #net['h6'].cmd("iperf3 -c 192.101.0.101 -t120")
    #net['h7'].cmd("iperf3 -c 192.101.0.101 -t120")
    #net['h8'].cmd("iperf3 -c 192.101.0.101 -t120")

    CLI(net)
    net.stop()

run()

