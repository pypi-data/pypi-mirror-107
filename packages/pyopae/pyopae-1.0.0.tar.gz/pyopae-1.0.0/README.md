# OPAE Python API based on DPDK
## 1. Background
OpenStack Cyborg needs to manage PAC (Programmable Acceleration Card) with the help of OPAE user space driver in DPDK. Cyborg is written in Python language,
which wants OPAE to provide Python API.  
OPAE chooses Python C API mechanism to wrap C function to Python method. In this package, there are one library file, one C source file and one C header file. All OPAE C APIs are archived in the library file, C files are just wrapper.
## 2. OPAE Python API
Python APIs provided to Cyborg are described in following sections.  
*Italic* argument in API is positional argument, **Bold** argument is keyword argument.
### 2.1 get_api_version()
Get API version.
### 2.2 set_log_level(*level*)
Set the console log level. If no argument is input, it does nothing at all. Current log level will be returned as a number described as below.
 + 0 - log is disabled
 + 1 - log of error message will be displayed in console (default)
 + 2 - log of error and warning message will be displayed in console
 + 3 - log of error, warning and information message will be displayed in console
 + 4 - all log will be displayed in console
### 2.3 set_log_file(*filename*, *clean*)
Set file for logging record. update progress and status. The clean argument has default value 0, means logging will be appended to the file, if you want to clean up the file before logging, set it to 1. If no arguments are input, log to file is disabled.
### 2.4 init_eal(*eal_parameters_string*)
Initialize DPDK run time environment. If no argument is input, default EAL parameters will be used. Please refer to **DPDK user guide** for valid parameter string. A number will be returned as the initialization result, 0 or positive value stands for success, negative value means failure.
 + The default EAL parameters is "**-n 4 --proc-type=auto**"
 + If you want to close EAL, PMD and OPAE log information, you can use parameters like "**-n 4 --proc-type=auto --log-level eal,0 --log-level pmd,0 --log-level driver.raw.init,0**"
 + If you want to open EAL, PMD and OPAE log information for debug, you can use parameters like "**-n 4 --proc-type=auto --log-level eal,8 --log-level pmd,8 --log-level driver.raw.init,8**"
### 2.5 get_proc_type()
Get the current process type of DPDK run time environment. A number described below will be returned.
 + -1 - DPDK is not running in current process, you need to call init_eal() method to start DPDK
 + 0 - DPDK is running as the primary instance in current process
 + 1 - DPDK is running as the secondary instance in current process
### 2.6 enumerate(**vid**, **did**, **cid**, **sub_vid**, **sub_did**)
Get the specified FPGA handle. If no argument is input, all FPGAs of PAC N3000 card will be returned. Named arguments are described below.
 + vid - PCI vendor ID of the specified FPGA
 + did - PCI device ID of the specified FPGA
 + cid - PCI class ID of the specified FPGA
 + sub_vid - PCI device subsystem vendor ID of the specified FPGA
 + sub_did - PCI device subsystem device ID of the specified FPGA
### 2.7 unbind(*id*)
Unbind kernel driver from the specified FPGA. The id argument should be chosen from the list returned by enumerate() method. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.8 bind(*id*, *driver*)
Bind specified kernel driver to the specified FPGA. The id argument should be chosen from the list returned by enumerate() method. The driver argument should be a name of installed driver. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.9 probe(*id*)
Force DPDK to do PCI bus probe operation, FPGA is managed by OPAE user space driver after probe successfully. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.10 remove(*id*)
Remove the specified FPGA from the management of OPAE user space driver. The id argument should be chosen from the list returned by enumerate() method. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.11 get_property(*id*, *type*)
Get the property information from the specified FPGA. The id argument should be chosen from the list returned by enumerate() method. The type argument can be combination of below numbers. If no argument is input, all property information will be returned.
 + 1 - PCI information, to get this information, device need NOT to be probed
 + 2 - FME information, to get this information, device MUST be probed
 + 4 - Port information, to get this information, device MUST be probed
 + 8 - BMC (MAX10) information, to get this information, device MUST be probed
### 2.12 pr(**id**, **port**, **file**)
Partial reconfigure AFU in specified port. Named argument id should be chosen from the list returned by enumerate method. Named argument port is the port index. Named argument file is the AFU bitstream file to configure into FPGA. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.13 get_image_info(*file*)
Validate the FPGA image file and return the image information. If the file is valid, a dictionary data will be returned. None is returned if image is invalid.  
value of key **type** is defined as below:
 + 0 - FPGA (A10) image
 + 1 - BMC (MAX10) image
 + 2 - GBS (AFU) image
 + 3 - PR (AFU) image  
value of key **subtype** is defined as below:
 + 0 - update image, this one should be used to update FPGA or BMC firmware
 + 1 - cancellation image
 + 2 - root key hash-256 image
 + 3 - root key hash-384 image
### 2.14 flash(**id**, **file**)
Update FPGA or BMC flash with the specified image. Named argument id should be chosen from the list returned by enumerate method. Named argument file is the image file to be used. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.15 cancel(*id*)
Cancel FPGA or BMC flash update process. Named argument id should be chosen from the list returned by enumerate method. A number will be returned as the result, 0 stands for success, negative value means failure. The update process can only be cancelled when staging area is being writing.
### 2.16 get_parent(*id*)
Get the parent PCI device of the specified FPGA. The id argument should be chosen from the list returned by enumerate method. An id will be returned if found, returned None means parent is not present.
### 2.17 get_child(*id*)
Get the child PCI device of the specified FPGA. The id argument should be chosen from the list returned by enumerate method. An id list will be returned if found, returned null list means child is not present.
### 2.18 get_pf1(*id*)
Get the second physical function (PF1) device of specified FPGA. The id argument should be chosen from the list returned by enumerate method. An id list will be returned if found, returned null list means PF1 is not present.
### 2.19 reboot(*id*)
Reboot PAC card with specified FPGA. The id argument should be chosen from the list returned by enumerate method. A number will be returned as the result, 0 stands for success, negative value means failure.
### 2.20 get_status(*id*)
Get FPGA or BMC flash update status and progress. The id argument should be chosen from the list returned by enumerate method. A dictionary data will be returned. None is returned if failed.
value of key **status** is defined as below:
 + 0 - IDLE, no flash update is in progress
 + 1 - PREPARING, hardware is preparing to start flash update
 + 2 - READY, hardware is ready to accept update data and host is writing image data to staging area, value of key **progress** show the percentage of image writing. You can only cancel flash update at this process.
 + 3 - COPYING, hardware is copying image data from staging area to specified flash area, value of key **progress** show the percentage of image copying
 + 4 - DONE, flash update done
 + 5 - REBOOT, hardware is rebooting
### 2.21 get_phy_info(*id*)
Get information of retimers which are connected to the specified FPGA.
### 2.22 cleanup_eal()
Free resources used within DPDK run time environment. You must call it at the end of the process.
## 3. Usage
### 3.1 System configuration
 + Make sure VT-d is enabled in BIOS
 + Make sure "**intel_iommu=on**" can be found in /proc/cmdline
 + Add "**default_hugepagesz=1G hugepagesz=1G hugepages=16 hugepagesz=2M hugepages=1024 pci=realloc pci=assign-busses**" to kernel boot options
 + Install vfio-pci driver by "**modprobe vfio-pci**"
### 3.2 Example Code
```
    import threading
    from pyopae import fpga

    fpga_list = fpga.enumerate(did=0x0b30)
    if fpga_list is None or len(fpga_list) == 0:
        return
    pac = fpga_list[0]
    fpga.init_eal()
    fpga.bind(pac, "vfio-pci")
    fpga.probe(pac)
    prop = fpga.get_property(pac)
    if prop['port'][0]['afu_id'] != EXPECTED_AFU_ID:
        return
    thrd = threading.Thread(target=fpga.flash, args=(pac, 'vc.bin'))
    thrd.start()
    prog = fpga.get_status(pac)
    if prog['status'] == 0:
        fpga.reboot(pac)
    fpga.cleanup_eal()
```
## 4. Limitation
### 4.1 Cannot run without root privilege
You will encounter error condition when calling init_eal() if the process have no root privilege.
### 4.2 Secondary process needs to be shut down when primary process exits
You can call get_proc_type() to check current process is primary or secondary, there have only one primary process. If the primary process exits while secondary process is still running, you will encounter error condition when calling init_eal() in a new process.
### 4.3 Reboot PAC card can only be executed in primary process
You will encounter error condition when calling reboot() in secondary process.
### 4.4 Do not reboot PAC in sub-process of primary process
If you create sub-process from primary process by using multiprocessing.Process, you should not call reboot() in sub-process. You can reboot PAC in sub-thread of primary process.