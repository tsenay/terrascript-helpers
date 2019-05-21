from terrascript import Terrascript, provider
from terrascript.vsphere.r import vsphere_virtual_machine
from terrascript.vsphere.d import vsphere_datastore
from terrascript.vsphere.d import vsphere_datacenter
from terrascript.vsphere.d import vsphere_resource_pool
from terrascript.vsphere.d import vsphere_network
from terrascript.vsphere.d import vsphere_virtual_machine \
    as data_vsphere_virtual_machine
import logging


class TerrascriptVM:
    def __init__(self, name):
        self.name = name
        self.ts = Terrascript()

    def CreateResourceFile(self, filename):
        pass


class TerrascriptVSphereVM(TerrascriptVM):
    def __init__(self, name):
        TerrascriptVM.__init__(self, name)
        self.guestid = None
        self.cpu = None
        self.memory = None
        self.folder = None
        self.provider = None
        self.datacenter = None
        self.datastore = None
        self.template = None
        self.gateway = None
        self.disks = []
        self.networks = []
        self.interfaces = []
        self.iface_customization = []
        self.dns = []
        self.dns_suffix = []

    def dumpResourceFile(self):
        linuxOptions = {}
        linuxOptions["host_name"] = self.name
        linuxOptions["domain"] = self.domain
        linuxOptions["time_zone"] = self.timezone

        customize = {}
        customize["linux_options"] = linuxOptions
        customize["network_interface"] = self.iface_customization
        customize["ipv4_gateway"] = self.gateway
        customize["dns_server_list"] = self.dns
        customize["dns_suffix_list"] = self.dns_suffix

        clone = {}
        clone["template_uuid"] = self.template.id
        clone["linked_clone"] = False
        clone["customize"] = customize
        if self.folder != '':
            virtualMachine = vsphere_virtual_machine(
                'vm',
                name=self.name,
                resource_pool_id=self.pool.id,
                datastore_id=self.datastore.id,
                guest_id=self.guestid,
                folder=self.folder,
                num_cpus=str(self.cpu),
                memory=self.memory,
                network_interface=self.interfaces,
                disk=self.disks,
                clone=clone)
        else:
            virtualMachine = vsphere_virtual_machine(
                'vm',
                name=self.name,
                resource_pool_id=self.pool.id,
                datastore_id=self.datastore.id,
                guest_id=self.guestid,
                num_cpus=str(self.cpu),
                memory=self.memory,
                network_interface=self.interfaces,
                disk=self.disks,
                clone=clone)
        self.ts.add(virtualMachine)
        return self.ts.dump()

    def setVSphereConfig(self, host, username, password):
        logger = logging.getLogger()
        logger.debug("Set VSphere provider to {}".format(host))
        self.provider = provider(
            "vsphere",
            user=username,
            password=password,
            vsphere_server=host,
            allow_unverified_ssl=True)
        self.ts.add(self.provider)

    def setDatacenter(self, datacenter):
        logger = logging.getLogger()
        logger.debug("Set VSphere datacenter to {}".format(datacenter))
        self.datacenter = vsphere_datacenter(
            "dc",
            name=datacenter)
        self.ts.add(self.datacenter)

    def setDatastore(self, datastore):
        if not self.datacenter:
            raise Exception
        else:
            logger = logging.getLogger()
            logger.debug("Set VSphere datastore to {}".format(datastore))
            self.datastore = vsphere_datastore(
                "ds",
                name=datastore,
                datacenter_id=self.datacenter.id)
            self.ts.add(self.datastore)

    def setResourcePool(self, pool):
        if not self.datacenter:
            raise Exception
        else:
            logger = logging.getLogger()
            logger.debug("Set VSphere Resource Pool to {}".format(pool))
            self.pool = vsphere_resource_pool(
                "pool",
                name=pool,
                datacenter_id=self.datacenter.id)
            self.ts.add(self.pool)

    def setTemplate(self, template):
        if not self.datacenter:
            raise Exception
        else:
            logger = logging.getLogger()
            logger.debug("Set VSphere template to {}".format(template))
            self.template = data_vsphere_virtual_machine(
                "template",
                name=template,
                datacenter_id=self.datacenter.id)
            self.ts.add(self.template)

    def addDisk(self, size):
        idx = len(self.disks)
        logger = logging.getLogger()
        logger.debug("Add {}GB disk".format(size))
        if len(self.disks) == 0:
            unitNumber = 0
        else:
            unitNumber = 1
        self.disks.append({
            "label": "disk{}".format(idx+1),
            "size": size,
            "unit_number": unitNumber})

    def addSuffix(self, dns):
        self.dns_suffix.append(dns)

    def addDns(self, dns):
        logger = logging.getLogger()
        logger.debug("Add {} to DNS list".format(dns))
        self.dns.append(dns)

    def addNetworkInterface(self, dvp, ipaddr, cidr):
        if not self.datacenter:
            raise Exception
        else:
            logger = logging.getLogger()
            logger.debug("Add network card on {} DVP, with {}/{}".format(dvp, ipaddr, cidr))
            vnet = vsphere_network(
                dvp,
                name=dvp,
                datacenter_id=self.datacenter.id)
            self.networks.append(vnet)
            self.ts.add(vnet)
            self.interfaces.append({"network_id": vnet.id})
            self.iface_customization.append({
                "ipv4_address": ipaddr,
                "ipv4_netmask": cidr})
