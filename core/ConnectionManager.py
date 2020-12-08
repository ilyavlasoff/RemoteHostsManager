import paramiko
from paramiko import SSHClient
from models import ConnectionData
from core.CommandExecutor import CommandExecutor


class ConnectionManager:
    client = None

    @staticmethod
    def connect(connection_data):
        if not type(connection_data) is ConnectionData.ConnectionData:
            raise Exception('Wrong connection data type')
        ConnectionManager.client = SSHClient()
        ConnectionManager.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ConnectionManager.client.connect(hostname=connection_data.get_host(),
                       username=connection_data.get_username(),
                       password=connection_data.get_password(),
                       port=connection_data.get_port())
        return CommandExecutor(ConnectionManager.client)
