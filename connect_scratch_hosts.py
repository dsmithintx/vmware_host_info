from pyVim.connect import SmartConnect, Disconnect, GetSi, SmartConnectNoSSL
from pyVmomi import vmodl
from pyVmomi import vim
import atexit
import requests
import ssl

# Disabling urllib3 ssl warnings
requests.packages.urllib3.disable_warnings()
# Disabling SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

user = "user_name"
password = "passwd"
vcenter = "vcenter_name"
port = 443


# connect to vCenter
try:
    si = SmartConnect(host=vcenter, user=user, pwd=password, port=port)
    print('Good to go')
except:
    si = SmartConnectNoSSL(host=vcenter, user=user, pwd=password, port=port)
    print('Using NoSSL Connection...')


# Disconnect when completed
atexit.register(Disconnect, si)

content = si.RetrieveContent()

##### View Types as a dictionary    i.e. Get-View types, HostSystem, VirtualMachine, etc.
vim_types = {'datacenter': [vim.Datacenter],
             'dvs_name': [vim.dvs.VmwareDistributedVirtualSwitch],
             'datastore_name': [vim.Datastore],
             'resourcepool': [vim.ResourcePool],
             'host': [vim.HostSystem],
             'cluster': [vim.ClusterComputeResource],
             'vm': [vim.VirtualMachine],
             'dportgroup': [vim.DistributedVirtualPortgroup],
             'portgroup': [vim.Network]}


##### View Types                                    i.e. Get-View types, HostSystem, VirtualMachine, etc.
Datacenter = [vim.Datacenter]                       # Datacenter
VirtualMachine = [vim.VirtualMachine]               # VirtualMachine
HostSystem = [vim.HostSystem]                       # HostSystem
# ClusterComputeResource [vim.ClusterComputeResource]
ClusterComputeResource = [vim.ComputeResource]
Datastore = [vim.Datastore]                         # Datastore
Network = [vim.Network]                             # Network
# DistributedVirtualPortgroup
DvPG = [vim.DistributedVirtualPortgroup]
Folder = [vim.Folder]                               # Folder

name = 'esx_host_name'

# Host objects
print("Collecting host objects...")
host_systems = content.viewManager.CreateContainerView(
    content.rootFolder, HostSystem, True)                  # Get-View -ViewType HostSystem
hostView = host_systems.view

print("Stop")


def print_host_info(host):
    config = host.config
    hardware = host.hardware
    runtime = host.runtime
    summary = host.summary
    for i in summary.hardware.otherIdentifyingInfo:
        if isinstance(i, vim.host.SystemIdentificationInfo):
            serial_number = i.identifierValue
    # summary.config.name
    print(f"Name                                            : {host.name}")
    print(f"Manufacture                                     : {hardware.systemInfo.vendor}")
    print(f"Model                                           : {hardware.systemInfo.model}")
    print(f"Serial Number                                   : {serial_number}")
    print(f"uuid                                            : {hardware.systemInfo.uuid}")
    print(f"Cpu Sockets                                     : {hardware.cpuInfo.numCpuPackages}")
    print(f"Number of Cores                                 : {hardware.cpuInfo.numCpuCores}")
    print(f"Mem Size                                        : {hardware.memorySize}")
    print(f"Bios Version                                    : {hardware.biosInfo.biosVersion}")
    print(f"Bios Release                                    : {hardware.biosInfo.releaseDate}")
    print(f"ESXi Version                                    : {summary.config.product.version}")
    print(f"ESXi Build                                      : {summary.config.product.build}")
    print(f"ESXi API Version                                : {summary.config.product.apiVersion}")
    print(f"Product Full Name                               : {summary.config.product.fullName}")
    print(f"License Product Name                            : {summary.config.product.licenseProductName}")
    print(f"License Product Version                         : {summary.config.product.licenseProductVersion}")
    print(f"Product Vendor                                  : {summary.config.product.vendor}")
    print(f"Boot Time                                       : {summary.runtime.bootTime}")
    print(f"Overall Status                                  : {summary.overallStatus}")
    print(f"Connection State                                : {runtime.connectionState}")
    print(f"Maintenance Mode                                : {runtime.inMaintenanceMode}")
    print(f"Power State                                     : {runtime.powerState}")
    print(f"Standby Mode                                    : {runtime.standbyMode}")
    print(f"vMotion IP                                      : {config.vmotion.ipConfig.ipAddress}")
    print(f"vMotion SubnetMask                              : {config.vmotion.ipConfig.subnetMask}")

## Find host by Name
for host in host_systems.view:
    if name:
        if host.name == name:
            obj = host
            print_host_info(host)
            print(host.name)
            break
    else:
        obj = host
        break

print("End")
