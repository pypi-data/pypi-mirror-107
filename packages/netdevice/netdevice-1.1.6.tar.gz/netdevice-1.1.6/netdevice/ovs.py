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
import copy

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
        self.device = []

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

    def add_br (self, name, *args, **kwargs):
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
        ip = kwargs.pop("ip", []) #get the ip configuration of the bridge
        ports = kwargs.pop("port", []) # get the ports list
        # Create the kwargs
        command = 'ovs-vsctl --may-exist add-br %s' %(name)
        if kwargs:
            # If there is parameters, for example datapath_type, etc.
            command += ' -- set bridge %s' %(name)
            for k,v in kwargs.items():
                command += ' %s=%s' %(k,v)
                self[k] = v
        self.cmd(command) #execut the command.

        # delete the current offlow when it's created
        #if self["fail-mode"] == "secure":
        #    self.cmd("ovs-ofctl del-flows %s" %(name))

        if ip:
            # Configure the ip address for the address for route
            self.cmd('ip address add %s dev %s' %(ip, name))
            self.cmd('ip link set %s up' %(name))
            self.cmd('ovs-appctl ovs/route/add %s %s' %(ip, name))

        # Add self-port if any, it's port = xxx, or *args,
        ports = ports if (isinstance(ports, list)) else [ports]
        ports = ports if (not args) else ports.extend(args)
        for p in ports:
            self.add_port(name, **p)

    def add_port (self, bridge_name, name, **kwargs):
        '''
        Add self-port and do some configuration if necessary.
        '''
        command = 'ovs-vsctl add-port %s %s' %(bridge_name, name)
        ip = kwargs.pop("ip", []) #get the ip configuration of the bridge
        if kwargs:
            # If there is parameters, for example type=vxlan, etc.
            command += ' -- set interface %s' %(name)
            for k,v in kwargs.items():
                command += ' %s=%s' %(k,v)
        self.cmd(command) #execut the command.

        #If it's a normal interface, flush it to release its original ip address.
        if (kwargs.get("type", "normal") == "normal"):
            self.cmd("ip addr flush dev %s" %(name))

        if ip:
            # Configure the ip address for the address for route
            self.cmd('ip link set %s up' %(name))
            self.cmd('ip address add %s dev %s' %(ip, name))
            #self.cmd('ovs-appctl ovs/route/add %s %s' %(ip, name))
            if self["fail-mode"] == "secure":
                # Confiure the default offlow for self port with IP.
                self.ofctl_add_flow(bridge_name,
                    "priority=65535,arp,arp_tpa=%s actions=normal" %(ip.split("/")[0]),
                    "priority=1,ip,nw_dst=%s actions=normal" %(ip.split("/")[0]))

    def add_device (self, bridge_name, *args, **kwargs):
        '''
        connect devices to ovs, now only support container.
        '''
        # Add remote-device and it's peer self-port
        for arg in args:
            # allocate and add the device into the list
            self.device.append(arg["name"])

            dtype = arg.get("type", None)
            if dtype == "container":
                self.__add_container(bridge_name, **arg)

                macaddr = self.cmd(
                    "docker exec -it %s ip link show %s | grep link/ether"
                    %(arg["name"], arg["interface"]), log_level = 4)
                # be compatible with the old version.
                arg["mac"] = macaddr.split()[1]
                arg["ofport"] = self.ovs_get_container_ofport(arg["name"])
            elif dtype == "qemu-system-x86_64":
                self.__add_vm(**arg)
            else:
                self.log("device type %s is not supported now..." %(dtype))

            # Configure offlow for the same subnet
            if self["fail-mode"] == "secure":
                ipaddr = ipaddress.ip_interface(arg["ip"])
                self.ofctl_add_flow(bridge_name,
                    "priority=65535,arp,arp_tpa=%s actions=output:%s"
                    %(ipaddr.ip, arg["ofport"]),
                    "priority=60000,ip,nw_src=%s,nw_dst=%s actions=output:%s" 
                    %(ipaddr.network, ipaddr.ip, arg["ofport"]))

    def __add_container (self, bridge_name,
            name = "con1",
            type = "docker",
            host_dir = "/var/shared",
            container_dir = "/var/shared", 
            interface = "eth1",
            ip = "",
            vlan = None,
            **kwargs):
        '''
        Create a container and connect it to the bridge: bridge_name.
        '''
        #创建容器, 设置net=none可以防止docker0默认网桥影响连通性测试
        self.cmd('docker run --privileged -d --name %s --net=none -v %s:%s -it centos'
                %(name, host_dir, container_dir))
        #self.cmd(' docker exec -it con11 rpm -ivh /var/shared/tcpdump-4.9.3-1.el8.x86_64.rpm ')
        self.cmd('ovs-docker add-port %s %s %s --ipaddress=%s'
                %(bridge_name, interface, name, ip))

        # Configure vlan on self-port if the device has vlan configured.
        if vlan:
            self.cmd('ovs-vsctl set port %s tag=%d'
                    %(ovs_get_container_port(bridge_name, name = name), vlan))

    def __add_vm (self, mask = None,
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
                for a in c.split(",", 1):
                    k,v = ("=" in a) and a.split("=", 1) or (a, True)
                    tmp_dic[k.strip()] = (isinstance(v, str)) and v.strip() or v
                all_chardev[tmp_dic["id"]] = "-chardev %s" %(c)
            #print(all_chardev)
            for n in netdev:
                # Parse the netdev to find its type.
                tmp_dic = {}
                for a in n.split(",", 1):
                    k,v = ("=" in a) and a.split("=", 1) or (a, True)
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
                for a in d.split(",", 1):
                    k,v = ("=" in a) and a.split("=", 1) or (a, True)
                    tmp_dic[k.strip()] = (isinstance(v, str)) and v.strip() or v
                cmd += " %s -device %s" %(all_netdev[tmp_dic["netdev"]], d)
        print(cmd)
        #val = os.system(cmd + "&")
        #self.cmd("whoami")
        #self.cmd(cmd)

    def add_gateway (self, bridge_name, gw, *args):
        '''
        Add some flows to ofproto
        '''
        vxlan_port = None # Get the vxlan at first.
        for d in args:
            if d["type"] == "vxlan":
                vxlan_port = self.ovs_get_interface(d["name"], "ofport")
                break
        for d in args:
            if d["type"] != "vxlan":
                if ((d["name"] not in self.device) and (not vxlan_port)):
                    # d is not on host, but there is no vxlan given.
                    self.log("Error: there is no vxlan to remote device: %s!"
                            %(d["name"]), bg_color = "red")
                    return
                self.ofctl_add_flow(bridge_name,
                    "priority=10,ip,nw_dst=%s,action=mod_dl_src:%s,"
                    "mod_dl_dst:%s,dec_ttl,output:%s"
                    %(d["ip"].split("/")[0], gw["mac"], d["mac"],
                        (d["name"] in self.device) and d["ofport"] or vxlan_port))

    def add_vtep (self, bridge_name, vtep, *args):
        '''
        Add some flows remote devices(*args): 从本主机上到达所有*args的包，全
        部经由vtep
        '''
        if self["fail-mode"] != "secure":
            #Don't need configure vtep explicitly in standalone mode.
            return
        for arg in args:
            ip = ipaddress.ip_interface(arg["ip"])
            vxlan_port = self.ovs_get_interface(vtep["name"], "ofport")
            self.ofctl_add_flow(bridge_name,
                    "priority=65535,arp,arp_tpa=%s actions=output:%s"
                    %(ip.ip, vxlan_port),
                    "priority=60000,ip,nw_src=%s,nw_dst=%s actions=output:%s" 
                    %(ip.network, ip.ip, vxlan_port))

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
                external_ids = self.ovs_get_interface(p.strip(), "external_ids")
                external_ids = external_ids.strip("{} \t\r\n")
                if ("=" in external_ids):
                    # Parse external_ids: {container_id=con13, container_iface=eth1}
                    i = {}
                    for a in external_ids.split(",", 1):
                        k,v = a.split("=", 1)
                        i[k.strip()] = v.strip()
                    if (i.get("container_id", None)):
                        self.cmd('docker stop %s' %(i["container_id"]))
                        self.cmd('docker rm %s' %(i["container_id"]))
            self.cmd("ovs-vsctl del-br %s" %(b.strip()))
        self.cmd('ovs-vsctl show')
        self.cmd('ovs-ctl stop')

    def ovs_get_interface (self, interface, attribute = None):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        if attribute:
            result = self.cmd("ovs-vsctl get interface %s %s"
                    %(interface, attribute))
            return result.strip()

        i = {}
        result = self.cmd("ovs-vsctl list interface %s" %(interface),
                log_level=4)
        for p in StringIO(result).readlines():
            k,v = p.split(":", 1)
            i[k.strip()] = v.strip()

        #return attribute and i.get(attribute, None) or i
        return i

    def ovs_get_container_ofport (self, name, **kwargs):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        bridges = self.cmd("ovs-vsctl list-br", log_level=4)
        for b in StringIO(bridges).readlines():
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()), log_level=4)
            for p in StringIO(ports).readlines():
                i = self.ovs_get_interface(p.strip())
                if (name in i.get("external_ids", None)):
                    return i.get("ofport", None)
        return None

    def ovs_get_container_port (self, name, **kwargs):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        bridges = self.cmd("ovs-vsctl list-br", log_level=4)
        for b in StringIO(bridges).readlines():
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()), log_level=4)
            for p in StringIO(ports).readlines():
                i = self.ovs_get_interface(p.strip())
                if (name in i.get("external_ids", None)):
                    return i.get("name", None)
        return None

    def ofctl_add_flow (self, bridge_name, *args, **kwargs):
        '''
        Add some flows to ofproto
        '''
        for table in args:
            table = filter(lambda x: (x.strip()) and (x.strip()[0] != '#'),
                    StringIO(table.strip()).readlines())
            for l in table:
                # remove the line starting with '#'
                l = l.strip()
                if l[0] !=  "#":
                    self.cmd('ovs-ofctl add-flow %s "%s"' %(bridge_name, l))
        return None

    def ping_test (self, src, dst):
        '''
        Add some flows to ofproto
        '''
        if src["type"] == "container":
            result = self.cmd('docker exec -it %s ping %s -c 1' %(src["name"],
                dst["ip"].split("/")[0]))
        else:
            result = None

        if "received, 0% packet loss," in result:
            self.log("PASS: %s ping %s, %s -> %s!" %(src["name"],
                dst["name"], src["ip"].split("/")[0],
                dst["ip"].split("/")[0]),
                bg_color = "green")
            return True
        else:
            self.log("FAIL: %s ping %s, %s -> %s!" %(src["name"],
                dst["name"], src["ip"].split("/")[0],
                dst["ip"].split("/")[0]),
                bg_color = "red")
            return False

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

