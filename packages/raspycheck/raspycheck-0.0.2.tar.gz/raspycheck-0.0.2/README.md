# raspycheck

**raspycheck** is a small tool to grab infos from and execute commands on a Raspberry Pi via SSH.

**raspycheck** is in an early alpha stage!

## Usage:

```python
from raspycheck import RasPyCheck

rpc = RasPyCheck(ip='ip', user='username', password='password', persist=False) # Setting persist to True keeps the connection open

# Commands to grab data from the RPI
ip = rpc.get_rpi_ip()
hostname = rpc.get_rpi_hostname()
cpu_temp = rpc.get_rpi_cpu_temp()
usb_devices = rpc.get_rpi_usb_devices()
rpi_version = rpc.get_rpi_version()
free_mem = rpc.get_rpi_free_memory()
total_mem = rpc.get_rpi_total_memory()
essids = rpc.get_rpi_available_essids()
date = rpc.get_rpi_date()
installed_packages = rpc.get_rpi_list_installed_packages()

all_infos = rpc.get_all_rpi_info()

# Commanding the Pi

rpc.cmd_reboot_pi()

# Generic stuff

output = rpc.run_command_get_output('pwd') # executes pwd on the RPI and returns the output
return_code = rpc.run_command_get_return_code('pwd') # executes pwd on the RPI and returns the return code

# Only when persist=True:

rpc.close_instance_client() # closes SSH client

```

## Supported Versions
raspycheck is currently only tested with Python3.9

## TODO:

- Extend errorhandling
- Extend functionality
- Add tests
- Relax/Check dependencies
- ...
