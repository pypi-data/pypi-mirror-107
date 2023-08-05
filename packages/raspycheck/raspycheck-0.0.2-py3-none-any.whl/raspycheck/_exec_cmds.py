import Lib

__methods__ = []
register_method = Lib.register_method(__methods__)

@register_method
def cmd_reboot_pi(self):
    """
    Reboots RPI

    :returns: Return code of reboot cmd
    """
    ret = self.run_command_get_return_code('reboot')
    return ret
