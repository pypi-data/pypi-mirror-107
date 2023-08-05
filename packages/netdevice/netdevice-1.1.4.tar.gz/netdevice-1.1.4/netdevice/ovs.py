#!/usr/bin/env python3

from netdevice import linux
import simplejson as json
import pexpect
import xmltodict
import ipaddress
import random
from lxml import etree
try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO
import sys, os, time
import collections
import tempfile

class OvsHost(linux.LinuxDevice):
    '''
    OvsHost is a linux host with OpenvSwitch installed. You can build the
    topology and run test on it.

    Now it integerate the docker and can connect the container automatically.
    '''
    def __init__ (self, server = None, **kwargs):
        '''
        Connect the host and start the OVS.
        '''

        linux.LinuxDevice.__init__(self, server, **kwargs)

        # start the docker if it's not running
        num = self.cmd('ps -ef | grep -w ovs-vswitchd | grep -v grep | wc -l')
        if num and int(num) <= 0:
            self.cmd('ovs-ctl start')
            self.cmd('ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true')
            self.log("Setup OVS complete")

        self["vlog"] = self["vlog"] and int(self["vlog"]) or -1
        if (self["vlog"] >= 0):
            self.cmd('echo > /usr/local/var/log/openvswitch/ovs-vswitchd.log')
            #self.cmd('echo > /usr/local/var/log/openvswitch/ovsdb-server.log')
            if (self["vlog"] == 0):
                self.cmd('ovs-appctl vlog/set ANY:file:emer')
            elif (self["vlog"] == 1):
                self.cmd('ovs-appctl vlog/set ANY:file:err')
            elif (self["vlog"] == 2):
                self.cmd('ovs-appctl vlog/set ANY:file:warn')
            elif (self["vlog"] == 3):
                self.cmd('ovs-appctl vlog/set ANY:file:info')
            elif (self["vlog"] >= 4):
                self.cmd('ovs-appctl vlog/set ANY:file:dbg')

        # start the docker if it's not running
        num = self.cmd('ps -ef | grep -w dockerd | grep -v grep | wc -l')
        if num and int(num) <= 0:
            self.cmd('systemctl start docker')
        self.log("Setup docker complete")

    def __del__(self):
        '''
        Get the trace file.
        Don't stop the OVS or docker.
        '''
        # postconfig
        self.log("%s.%s(%s), finish in %.2f seconds\n" %(self.__class__.__name__,
            sys._getframe().f_code.co_name,
            self.version,
            time.time() - self.start_time))

        if (self["vlog"] >= 0):
            #self.get_file('/usr/local/var/log/openvswitch/ovsdb-server.log',
            #        "%s_ovsdb-server.log" %(self["name"]))
            self.get_file('/usr/local/var/log/openvswitch/ovs-vswitchd.log',
                    "%s_ovs-vswitched.log" %(self["name"]))

    def add_br (self, bridge, *args, **kwargs):
        '''
        Add a bridge and build the subnet.

        A bridge looks like this:

            vm1_vxlan0 = {"name": "vxlan0",
                           "type": "vxlan",
                           "options:remote_ip": "192.168.63.113",
                           "options:key": "flow" }
            vm1_br_int = {"name": "br-int",
                          "datapath_type": "netdev",
                          "port": [ vm1_vxlan0, ]}

        And devices look like this:

            con1 = {"name": "con1",
                    "type": "container",
                    "interface": "eth1",
                    "ip": "10.208.1.11/24"}

        '''
        bridge_name = bridge.pop("name", None) #get bridge name
        ip = bridge.pop("ip", []) #get the ip configuration of the bridge
        ports = bridge.pop("port", []) # get the ports list
        # Create the bridge
        command = 'ovs-vsctl --may-exist add-br %s' %(bridge_name)
        if bridge:
            # If there is parameters, for example datapath_type, etc.
            command += ' -- set bridge %s' %(bridge_name)
            for k,v in bridge.items():
                command += ' %s=%s' %(k,v)
        self.cmd(command) #execut the command.
        if ip:
            # Configure the ip address for the address for route
            self.cmd('ip address add %s dev %s' %(ip, bridge_name))
            self.cmd('ip link set %s up' %(bridge_name))
            self.cmd('ovs-appctl ovs/route/add %s %s' %(ip, bridge_name))

        # Add self-port if any
        ports = ports if (isinstance(ports, list)) else [ports]
        for p in ports:
            self.add_port(bridge_name, **p)

        # Add remote-device and it's peer self-port
        #for d in args:
        #    print("d: " %(d))
        #    self.add_device(bridge_name, **d)

    def add_port (self, bridge_name, name, **kwargs):
        '''
        Add self-port and do some configuration if necessary.
        '''
        command = 'ovs-vsctl add-port %s %s' %(bridge_name, name)
        if kwargs:
            # If there is parameters, for example type=vxlan, etc.
            command += ' -- set interface %s' %(name)
            for k,v in kwargs.items():
                command += ' %s=%s' %(k,v)
        self.cmd(command) #execut the command.

    def add_vm (self, mask = None,
            type = "qemu-system-x86_64",
            name = "vm1",
            cpu = "host", 
            smp = "sockets=1,cores=1",
            m = "1024M", 
            hda = None,
            boot = "c",
            net = "none",
            pidfile = "/tmp/vm1.pid",
            monitor = "unix:/tmp/vm1monitor,server,nowait",
            object = "memory-backend-file,id=mem,size=1024M,mem-path=/dev/hugepages,share=on",
            numa = "node,memdev=mem",
            chardev = None,
            netdev = None,
            device = None,
            **kwargs):
        '''
        taskset 8 qemu-system-x86_64 -name $VM_NAME -cpu host -smp sockets=1,cores=1 -m 1024M -hda $QCOW2_IMAGE -boot c -enable-kvm -net none -no-reboot -pidfile /tmp/vm1.pid -monitor unix:/tmp/vm1monitor,server,nowait -object memory-backend-file,id=mem,size=1024M,mem-path=/dev/hugepages,share=on -numa node,memdev=mem -mem-prealloc -chardev socket,id=char1,path=$VHOST_SERVER_PATH,server -netdev type=vhost-user,id=net1,chardev=char1,vhostforce -device virtio-net-pci,netdev=net1,mac=00:00:00:00:00:01,csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off
        '''
        cmd = mask and ("taskset %s %s" %(mask, type)) or type
        cmd += " -name %s -cpu %s -smp %s -m %s -hda %s -boot %s"\
                %(name, cpu, smp, m, hda, boot)
        if kwargs.get("enable-kvm", True):
            cmd += " -enable-kvm"
        if kwargs.get("no-reboot", True):
            cmd += " -no-reboot"
        if kwargs.get("mem-prealloc", True):
            cmd += " -mem-prealloc"
        cmd += " -net %s -pidfile %s -monitor %s -object %s -numa %s"\
                %(net, pidfile, monitor, object, numa)

        if (device):
            # if the chardev/netdev/device are given, use them
            chardev = isinstance(chardev, list) and chardev or [chardev]
            netdev = isinstance(netdev, list) and netdev or [netdev]
            device = isinstance(device, list) and device or [device]
            all_chardev = {}
            all_netdev = {}
            for c in chardev:
                # Parse the chardev to find its type.
                tmp_dic = {}
                for a in c.split(","):
                    k,v = ("=" in a) and a.split("=") or (a, True)
                    tmp_dic[k.strip()] = (isinstance(v, str)) and v.strip() or v
                all_chardev[tmp_dic["id"]] = "-chardev %s" %(c)
            #print(all_chardev)
            for n in netdev:
                # Parse the netdev to find its type.
                tmp_dic = {}
                for a in n.split(","):
                    k,v = ("=" in a) and a.split("=") or (a, True)
                    tmp_dic[k.strip()] = (isinstance(v, str)) and v.strip() or v
                if ("chardev" in tmp_dic):
                    all_netdev[tmp_dic["id"]] = " %s -netdev %s"\
                            %(all_chardev[tmp_dic["chardev"]], n)
                else:
                    all_netdev[tmp_dic["id"]] = "-netdev %s" %(n)
            #print(all_netdev)
            for d in device:
                # Parse the device to find its type.
                tmp_dic = {}
                for a in d.split(","):
                    k,v = ("=" in a) and a.split("=") or (a, True)
                    tmp_dic[k.strip()] = (isinstance(v, str)) and v.strip() or v
                cmd += " %s -device %s" %(all_netdev[tmp_dic["netdev"]], d)
        print(cmd)
        #val = os.system(cmd + "&")
        #self.cmd("whoami")
        #self.cmd(cmd)

    def add_devices (self, bridge_name, *args, **kwargs):
        '''
        connect devices to ovs, now only support container.
        '''
        # Add remote-device and it's peer self-port
        for d in args:
            dtype = d.get("type", None)
            if dtype == "docker":
                # Create a container and the self-port
                ports = d.pop("port", []) # get the ports list
                for p in ports:
                    self.cmd('docker run --privileged -d --name %s -v %s:%s -it centos'
                            %(p["name"], p.get("host_dir", "/var/shared"),
                              p.get("container_dir", "/var/shared")))

                    #Allocate the interface/ipaddress and connect it to ovs bridge
                    self.cmd('ovs-docker add-port %s %s %s --ipaddress=%s'
                            %(bridge_name, p["interface"], p["name"], p["ip"]))
            elif dtype == "qemu-system-x86_64":
                # Create ifup/ifdown script
                self.add_vm(**d)
            else:
                self.log("device type %s is not supported now..." %(dtype))

            # Configure vlan on self-port if the device has vlan configured.
            #if d.get("vlan", None):
            #    self.cmd('ovs-vsctl set port %s tag=%d'
            #            %(__ovs_get_port(bridge_name, name = name), d["vlan"]))

    def del_br (self, *args, **kwargs):
        '''
        Delete the bridge and all the connected devices(containers).

        If bridge name is not given, delete all the bridges.
        '''
        # delete all the bridges in the OVS
        bridges = args and args or self.cmd("ovs-vsctl list-br")
        for b in StringIO(bridges).readlines():
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()))
            for p in StringIO(ports).readlines():
                # delete all the devices(container/vm/physical) connectting to.
                external_ids = self.__get_external_ids(p.strip())
                #print("external_ids: %s" %(external_ids))
                if (external_ids.get("container_id", None)):
                    self.cmd('docker stop %s' %(external_ids["container_id"]))
                    self.cmd('docker rm %s' %(external_ids["container_id"]))
            self.cmd("ovs-vsctl del-br %s" %(b.strip()))
        self.cmd('ovs-vsctl show')
        self.cmd('ovs-ctl stop')

    def __get_external_ids (self, port = None):
        '''
        parse external_ids and return the dictionary.
        '''
        external_ids = {}
        command = "ovs-vsctl list interface"
        if port:
            command += " %s" %(port)
        command += " | awk -F: '/container_id/ {print $2}'"

        result = self.cmd(command)
        for line in StringIO(result).readlines():
            for a in line.strip("{} \t\r\n").split(","):
                k,v = a.split("=")
                external_ids[k.strip()] = v.strip()
        #print("external_ids: %s" %(external_ids))
        return external_ids

    def __ovs_get_port (self, bridge, name, **kwargs):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''
        ports = self.cmd("ovs-vsctl list-ports %s" %(bridge))
        for p in StringIO(ports).readlines():
            external_ids = self.__get_external_ids(p.strip())
            if (external_ids.get("container_id", None) == name):
                return p.strip()
        return None

    def ovs_add_flows (self, bridge, *args, **kwargs):
        '''
        Add some flows to ofproto
        '''

        for table in args:
            table = filter(lambda x: (x.strip()) and (x.strip()[0] != '#'),
                    StringIO(table.strip()).readlines())
            for l in table:
                # remove the line starting with '#'
                self.cmd('ovs-ofctl add-flow %s "%s"'
                        %(bridge["name"], l.strip()))
        return None

    def ovs_get_topology (self, *args, **kwargs):
        '''
        Destroy the topology:

            * Destroy the OVS and all its bridges.
            * Destroy all the devices connected to it if given in the *args.
        '''
        # delete all the bridges in the OVS
        #topology = {"name": self["name"], "bridges": [] }
        topology = []
        bridges = self.cmd("ovs-vsctl list-br")
        for b in StringIO(bridges).readlines():
            #print("Bridge %s" %(b.strip()))
            topology.append("Bridge %s" %(b.strip()))
            #bridge = {"name": b.strip(), "ports": []}
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()))
            for p in StringIO(ports).readlines():
                external_ids = self.__get_external_ids(p.strip())
                if (not external_ids):
                    topology.append("    Port %s, external_ids: %s"
                            %(p.strip(), external_ids.strip()))

                options = self.cmd(
                 "ovs-vsctl list interface %s | awk -F: '/options/ {print $2}'"
                  %(p.strip()))
                if (options.strip() != "{}"):
                    topology.append("    Port %s, options: %s"
                            %(p.strip(), options.strip()))

                link_speed = self.cmd(
                 "ovs-vsctl list interface %s | awk -F: '/link_speed/ {print $2}'"
                  %(p.strip()))
                if (options.strip() != "[]"):
                    topology.append("    Port %s, link_speed: %s"
                            %(p.strip(), link_speed.strip()))
                #port = {"name": p.strip(), "interface": p.strip()}
                #print("    Port %s %s" %(p.strip(), external_ids.strip()))
                #bridge["ports"].append(port)
            #topology["bridges"].append(bridge)
        #self.log("container: %s\n" %(json.dumps(topology, indent=4)))
        for i in topology:
            print(i)

if __name__ == '__main__':
    '''
    #topology：
        (vr1)vrl1 -- vsl1(dvs1)vsl1 -- vrl1(vr1)
    '''

    vm1 = OvsHost("ssh://root:sangfor@172.93.63.111", name = "vm1",
            log_color = "red", log_level = options.log_level)
    vm1_br_int = {"name": "br-int", "datapath_type": "netdev",
            "port": [ {"name": "vxlan0", "type": "vxlan",
                "options:remote_ip": "192.168.63.113", "options:key": "flow" }]}
    vm1_br_phy = {"name": "br-phy", "datapath_type": "netdev",
            "other_config:hwaddr": "fe:fc:fe:b1:1d:0b",
            }
    vm1_eth1 = {"name": "eth1", "type": "phy", "ip": "192.168.63.111/16"}
    con = []
    for i in range(4):
        con.append({"name": "con%d"%(i), "type": "container", "interface": "eth1",
            "ip": "10.208.1.%d/24" %(10+i)})
    vm1.log("container: %s\n" %(json.dumps(con, indent=4)))
    vm1.cmd('ovs-vsctl show')

    vm1.ovs_connect(vm1_br_int, con[0], con[1])
    vm1.ovs_connect(vm1_br_phy, vm1_eth1)
    vm1.cmd('ovs-vsctl show')

