#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'bird -c '+ self.name +'.conf -s '+ self.name +'.ctl' )
		
    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        self.cmd( 'birdc -s '+ self.name +'.ctl down' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):		
		
        r1 = self.addHost( 'r1', cls=LinuxRouter, ip='192.0.1.2/24')
        r2 = self.addHost( 'r2', cls=LinuxRouter, ip='195.0.1.1/24')
        r3 = self.addHost( 'r3', cls=LinuxRouter, ip='196.0.1.1/24')
        r4 = self.addHost( 'r4', cls=LinuxRouter, ip='197.0.1.2/24')
        
	    
        h1 = self.addHost( 'h1', cls=LinuxRouter, ip='192.0.1.1/24')
        h2 = self.addHost( 'h2', cls=LinuxRouter, ip='197.0.1.1/24')
        
        self.addLink(h1, r1, intfName1='h1-eth1', intfName2='r1-eth1', params1={ 'ip' : '192.0.1.1/24' }, params2={ 'ip' : '192.0.1.2/24' })
        self.addLink(h2, r4, intfName1='h2-eth1', intfName2='r4-eth3', params1={ 'ip' : '197.0.1.1/24' }, params2={ 'ip' : '197.0.1.2/24' })
        self.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1', params1={ 'ip' : '195.0.1.1/24' }, params2={ 'ip' : '195.0.1.2/24' })
        self.addLink(r3, r4, intfName1='r3-eth2', intfName2='r4-eth2', params1={ 'ip' : '196.0.1.1/24' }, params2={ 'ip' : '196.0.1.2/24' })
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={ 'ip' : '193.0.1.1/24' }, params2={ 'ip' : '193.0.1.2/24' })
        self.addLink(r1, r3, intfName1='r1-eth3', intfName2='r3-eth1', params1={ 'ip' : '194.0.1.1/24' }, params2={ 'ip' : '194.0.1.2/24' })			
		

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, waitConnected=True, link = TCLink )
    net.start()
	
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
