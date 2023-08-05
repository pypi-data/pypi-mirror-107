import sys, os, socket, termcolor, logging
from paramiko import SSHClient
from .Lib import Lib
from ._get_info import _get_info
from ._exec_cmds import _exec_cmds

@Lib.add_methods_from(_get_info)
@Lib.add_methods_from(_exec_cmds)
class RasPyCheck():
    logger = None
    loglevel = None
    ip = None
    user = None
    password = None
    ssh_client = None
    keep_connection_open = None

    def __init__(self, ip, user, password, persist=False, debug=False):
        """
        Initializes an instance of RasPyCheck

        :param str ip: IP of the Raspberry Pi
        :param str user: Username to connect with
        :param str password: Password to connect with
        :param boolean persist: Keep connection alive (defaults to False)
        :param boolean debug: Gives more output (loglevel debug)
        """
        self.set_loglevel(debug)
        self.init_logger()
        self.ip = ip
        self.user = user
        self.password = password
        self.keep_connection_open = persist
        if self.keep_connection_open == True:
            self.setup_client()

    def set_loglevel(self, debug):
        """
        Sets loglevel to eiter DEBUG or ERROR
        """
        if debug == True:
            self.loglevel = logging.DEBUG
        else:
            self.loglevel = logging.ERROR

    def init_logger(self):
        """
        Initializes the logger
        """
        handler = logging.StreamHandler(sys.stdout)
        frm = logging.Formatter("[raspycheck] {asctime} - {levelname}: {message}", "%d.%m.%Y %H:%M%S", style="{")
        handler.setFormatter(frm)
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(self.loglevel)

    def setup_client(self):
        """
        Creates a SSHClient instance and keeps it open until closed by calling
        self.close instance
        """
        self.ssh_client = SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.connect(self.ip, username=self.user, password=self.password)

    def close_instance_client(self):
        """
        Closes instance client
        """
        if self.ssh_client is not None:
            self.ssh_client.close()

    def cleanup_cmd_execution(self, stdin, stdout, stderr, client):
        """
        Cleanup after cmd execution. Closes streams and client if the latter is not persistant.

        :param paramiko.channel.ChannelStdinFile stdin: SSH stdin object
        :param paramiko.channel.ChannelFile stdout: SSH stdout object
        :param paramiko.channel.ChannelStderrFile stderr: SSH stderr object
        :param SSHClient client: Instance of SSHClient used for command execution, will only get close if not persisted
        """
        stdin.close()
        stdout.close()
        stderr.close()
        if self.ssh_client == None:
            client.close()

    def get_client(self):
        """
        Returns either the instance SSHClient or creates a new, temporary one
        """
        if self.ssh_client is not None:
            client = self.ssh_client
        else:
            client = SSHClient()
            client.load_system_host_keys()
            client.connect(self.ip, username=self.user, password=self.password)
        return client

    def run_command_get_output(self, cmd):
        """
        Executes command on raspberry pi and returns STDOUT

        :param str cmd: Command to execute on the Pi
        :returns: Response from the command
        """
        client = self.get_client()
        stdin, stdout, stderr = client.exec_command(cmd)
        response = stdout.read().decode("utf8")
        error = stderr.read().decode("utf8")
        self.logger.debug(response)
        if error is not None and error != "":
            self.logger.error(termcolor.colored(error, "red"))
        self.cleanup_cmd_execution(stdin, stdout, stderr, client)
        return response

    def run_command_get_return_code(self, cmd):
        """
        Executes command on Raspberry Pi and returns return code

        :param str cmd: Command to execute
        :returns: Return code from command execution
        """
        client = self.get_client()
        stdin, stdout, stderr = client.exec_command(cmd)
        return_code = stdout.channel.recv_exit_status()
        error = stderr.read().decode("utf8")
        self.logger.debug(return_code)
        if error is not None and error != "":
            self.logger.error(termcolor.colored(error, "red"))
        self.cleanup_cmd_execution(stdin, stdout, stderr, client)
        return return_code
