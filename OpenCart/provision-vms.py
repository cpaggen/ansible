from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import sys
import ssl
import xmlrpclib

si = None
username = "root"
password = "vmware"
vcenter = "10.48.58.109"
cobIp = "10.48.82.82"
cobUser = "cobbler"
cobPassword = "cisco"

def add_nic(content, vm, network, macAddress):
    spec = vim.vm.ConfigSpec()
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device = vim.vm.device.VirtualE1000()

    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = 'automated'

    nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect = False
    nic_spec.device.backing.network = GetNet(content, network)
    nic_spec.device.backing.deviceName = network

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = True
    nic_spec.device.connectable.status = 'untried'
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'manual'
    nic_spec.device.macAddress = macAddress
    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    e = vm.ReconfigVM_Task(spec=spec)
    print "\t\tNIC added to VM"

def getNicMac(vm):
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard):
            nic.device = dev


def addDiskVM(vm, disk_size):
    spec = vim.vm.ConfigSpec()
    scsi_ctr = vim.vm.device.VirtualDeviceSpec()
    scsi_ctr.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    scsi_ctr.device = vim.vm.device.VirtualLsiLogicController()
    scsi_ctr.device.deviceInfo = vim.Description()
    scsi_ctr.device.slotInfo = vim.vm.device.VirtualDevice.PciBusSlotInfo()
    scsi_ctr.device.slotInfo.pciSlotNumber = 16
    scsi_ctr.device.controllerKey = 100
    scsi_ctr.device.unitNumber = 3
    scsi_ctr.device.busNumber = 0
    scsi_ctr.device.hotAddRemove = True
    scsi_ctr.device.sharedBus = 'noSharing'
    scsi_ctr.device.scsiCtlrUnitNumber = 7

    unit_number = 0
    controller = scsi_ctr.device
    disk_spec = vim.vm.device.VirtualDeviceSpec()
    disk_spec.fileOperation = "create"
    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    disk_spec.device = vim.vm.device.VirtualDisk()
    disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
    disk_spec.device.backing.diskMode = 'persistent'
    disk_spec.device.backing.thinProvisioned = True
    disk_spec.device.backing.fileName = '%s %s.vmdk' % \
    ( datastorePath, vmName )
    disk_spec.device.unitNumber = unit_number
    disk_spec.device.capacityInKB = disk_size * 1024
    disk_spec.device.controllerKey = controller.key


    dev_changes = []
    dev_changes.append( scsi_ctr )
    dev_changes.append( disk_spec )
    spec.deviceChange = dev_changes
    vm.ReconfigVM_Task(spec=spec)
    print "\t\t%sGB disk added to %s" % (disk_size, vm.config.name)

def GetNet(content, network):
    obj = None
    net_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.Network], True)
    for n in net_view.view:
        if n.name == network:
            net = n
            break
    return net

def GetVM(content, vm):
    obj = None
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine], True)
    for c in vm_view.view:
        if c.name == vm:
            vm = c
            break
    return vm

def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem], True)
    obj = host_view.view
    host_view.Destroy()
    return obj

def _create_char_spinner():
    """Creates a generator yielding a char based spinner.
    """
    while True:
        for c in '|/-\\':
            yield c

_spinner = _create_char_spinner()

def CreateVM(host, config):
    vm_folder = host.vm[0].parent
    resource_pool = host.vm[0].resourcePool
    task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)
    while task.info.state not in [vim.TaskInfo.State.success,
                                  vim.TaskInfo.State.error]:
        sys.stdout.write("\r\t%s %s" % ("creating VM", _spinner.next()))
        sys.stdout.flush()

def connectVC(user, vc, password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    try:
        si = SmartConnect(host=vcenter, user=username, pwd=password, sslContext=context)
    except IOError, e:
        print "Cannot connect - error {}".format(e)
        sys.exit(1)
    return si


def connectCobbler(ip, cobUser, cobPassword):
    url = "http://" + ip + "/cobbler_api"
    cobblerServer = xmlrpclib.Server(url)
    token = cobblerServer.login(cobUser, cobPassword)
    return cobblerServer, token

def insert_system_to_cobbler(CobblerServer, NodeName, MacAddress, IpAddress, \
        Gateway, Hostname, Profile, DnsName, token):
    system_id = CobblerServer.new_system(token)
    CobblerServer.modify_system(system_id, "name", NodeName, token)
    CobblerServer.modify_system(system_id, 'modify_interface', \
        {"macaddress-eth0": MacAddress, \
        "ipaddress-eth0": IpAddress, "dnsname-eth0": DnsName,}, token)
    CobblerServer.modify_system(system_id, "profile", Profile, token)
    CobblerServer.modify_system(system_id, "gateway", Gateway, token)
    CobblerServer.modify_system(system_id, "hostname", Hostname, token)
    # After modify, sync them to the system
    CobblerServer.save_system(system_id, token)

def powerThemUp(content, vmNames):
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()
    # Find the vm and power it on
    tasks = [vm.PowerOn() for vm in vmList if vm.name in vmNames]

#########################################################################################


si = connectVC(username, vcenter, password)
cob, token = connectCobbler(cobIp,cobUser, cobPassword)
content = si.RetrieveContent()
hosts = GetVMHosts(content)
for host in hosts:
    if host.name == "10.48.58.111":
        print "Found {} running {}".format(host.name, host.config.product.fullName)
        thisHost = host
        datastores = [datastore for datastore in thisHost.datastore]
        for datastore in datastores:
            if datastore.info.name == "Nimble-Lun-11":
                print "\tdatastore {} has {}Gb free space".format(datastore.info.name, datastore.info.freeSpace/1000000000)
                thisDatastore=datastore

vmName = "TA-lab-student-VM-"
cpu = 1
network = "Backbone"
diskSize = 16000
baseIp = "10.48.58."
vmNames=[]
numberOfVMs=4

for i in range(1,numberOfVMs+1):
    vmName= "TA-lab-student-VM-{}".format(i)
    vmNames.append(vmName)
    datastorePath = '[' + "Nimble-Lun-11" + '] ' + vmName
    vmxFile = vim.vm.FileInfo(logDirectory=None,
                              snapshotDirectory=None,
                              suspendDirectory=None,
                              vmPathName=datastorePath)
    config = vim.vm.ConfigSpec( name=vmName,
                                memoryMB=2048,
                                numCPUs=cpu,
                                files=vmxFile,
                                guestId="ubuntu64Guest",
                                version='vmx-07')

    CreateVM(thisHost, config)
    thisVM = GetVM(content, vmName)
    if thisVM:
        print "\t{} created".format(thisVM)
        macAddress="00:ca:fe:00:00:{:02X}".format(i)
        add_nic(content, thisVM, network, macAddress)
        addDiskVM(thisVM, diskSize)
        print "\t inserting system in Cobbler"
        ip = baseIp + str(24+i)
        insert_system_to_cobbler(cob, vmName, macAddress, ip, \
                         "10.48.58.1", vmName, "Ubuntu-16.04.3-server_x64-x86_64", \
                         vmName, token)
    else:
        print "Can't create or retrieve VM!"

cob.sync(token)
print "Cobbler synced!"
print "Powering up all VMs - check VC"
powerThemUp(content, vmNames)

Disconnect(si)
