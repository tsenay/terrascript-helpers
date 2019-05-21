from terrascriptobjects import TerrascriptVSphereVM
import json

VI_HOST = 'vsphere.domain.com'
VI_USER = 'vi_user'
VI_PASSWORD = 'vi_password'
DISK1_SIZE = "32"
DISK2_SIZE = "100"
IP_GATEWAY = '10.1.1.1'
DNS1 = '8.8.8.8'
DNS2 = '1.1.1.1'


def testTerrascriptVSphereVM():
    vm = TerrascriptVSphereVM('testVM')
    vm.setDatacenter('DC')
    vm.setDatastore('DS')
    vm.setVSphereConfig(VI_HOST, VI_USER, VI_PASSWORD)
    vm.setResourcePool('pool')
    vm.memory = '1024'
    vm.cpu = 2
    vm.guestid = 'rhel7_64Guest'
    vm.addDns(DNS1)
    vm.addDns(DNS2)
    vm.addSuffix('domain.com')
    vm.setTemplate('template')
    vm.folder = 'test'
    vm.gateway = IP_GATEWAY
    vm.timezone = 'Etc/Utc'
    vm.addDisk(DISK1_SIZE)
    vm.addDisk(DISK2_SIZE)
    vm.domain = "mydomain.com"
    vm.addNetworkInterface('dvp', '10.1.1.10', '24')
    data = vm.dumpResourceFile()
    obj = json.loads(data)
    assert type(obj) is dict
    assert obj['data'][0]['vsphere_datacenter']['dc']['name'] == 'DC'
    provider = obj['provider']['vsphere']['__DEFAULT__']
    assert provider['vsphere_server'] == VI_HOST
    assert provider['user'] == VI_USER
    assert provider['password'] == VI_PASSWORD
    vm = obj['resource']['vsphere_virtual_machine']['vm']
    disk0 = vm['disk'][0]
    assert disk0['label'] == 'disk1'
    assert disk0['size'] == DISK1_SIZE
    disk1 = vm['disk'][1]
    assert disk1['label'] == 'disk2'
    assert disk1['size'] == DISK2_SIZE
    iface1 = vm['network_interface'][0]
    assert iface1['network_id'] == "${data.vsphere_network.dvp.id}"
    assert not vm['clone']['linked_clone']
    customize = vm['clone']['customize']
    assert customize['ipv4_gateway'] == IP_GATEWAY
    assert type(customize['dns_server_list']) is list
    assert customize['dns_server_list'][0] == DNS1
    assert customize['dns_server_list'][1] == DNS2
