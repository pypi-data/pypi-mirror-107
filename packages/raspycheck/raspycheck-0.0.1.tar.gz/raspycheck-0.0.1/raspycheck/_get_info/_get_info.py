from raspycheck.Lib import Lib

__methods__ = []
register_method = Lib.register_method(__methods__)

@register_method
def get_rpi_ip(self):
    """
    Returns IPv4 and IPv6 addresses from the Pi

    :returns: String containing IPv4 and IPv6 addresses, seperated by space
    """
    rpip = self.run_command_get_output('hostname -I').replace("\n", "")
    return rpip

@register_method
def get_rpi_hostname(self):
    """
    Returns hostname from the Pi

    :returns: String containing hostname of the Pi
    """
    hostname = self.run_command_get_output('hostname').replace("\n", "")
    return hostname

@register_method
def get_rpi_cpu_temp(self):
    """
    Returns CPU temperature of the pi

    :returns: String containing CPU temperature of the RPI
    """
    temp = self.run_command_get_output('vcgencmd measure_temp').replace("\n", "").replace("temp=", "")
    return temp

@register_method
def get_rpi_usb_devices(self):
    """
    Returns a list of the currently connected USB devices of the Pi

    :returns: List with USB devices
    """
    devices = self.run_command_get_output('lsusb')
    devices = devices.split("\n")
    devices = list(filter(None, devices))
    return devices

@register_method
def get_rpi_version(self):
    """
    Returns version of RPI

    :returns: String with version information
    """
    version = self.run_command_get_output('cat /proc/version').replace("\n", "")
    return version

@register_method
def get_rpi_free_memory(self):
    """
    Returns info about how much free memory is available

    :returns: Free memory
    """
    memory = self.run_command_get_output('free').split()[9]
    return memory

@register_method
def get_rpi_total_memory(self):
    """
    Returns info about how much total memory is available

    :returns: Total memory
    """
    memory = self.run_command_get_output('free').split()[7]
    return memory

@register_method
def get_rpi_available_essids(self):
    """
    Returns list of ESSIDs available to the Pi

    :returns: List of ESSIDs
    """
    essids = self.run_command_get_output('iwlist wlan0 scan | grep ESSID')
    return essids

@register_method
def get_rpi_date(self):
    """
    Returns date and time as used by the Pi

    :returns: Date of the RPI
    """
    date = self.run_command_get_output('date').replace("\n", "")
    return date

@register_method
def get_rpi_list_installed_packages(self):
    """
    Returns list with installed packages
    """
    packages = self.run_command_get_output('dpkg --get-selections')
    return packages

@register_method
def get_all_rpi_info(self):
    """
    Returns dictionary with all available RPI information
    """
    return {
        'ip': self.get_rpi_ip(),
        'hostname': self.get_rpi_hostname(),
        'cpu_temp': self.get_rpi_cpu_temp(),
        'usb_devices': self.get_rpi_usb_devices(),
        'version': self.get_rpi_version(),
        'free_memory': self.get_rpi_free_memory(),
        'total_memory': self.get_rpi_total_memory(),
        'date': self.get_rpi_date()
    }
