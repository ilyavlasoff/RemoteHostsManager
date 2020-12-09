import paramiko
from paramiko import SSHClient
from models import ConnectionData
from core.CommandExecutor import CommandExecutor


class ConnectionManager:
    hold_clients = dict()

    @staticmethod
    def get_connection(key):
        conn = ConnectionManager.hold_clients.get(key)
        return conn

    @staticmethod
    def add_connection(key, connection_data):
        conn = ManagedItem(connection_data)
        ConnectionManager.hold_clients[key] = conn
        return conn


class ManagedItem:
    def __init__(self, connection_data):
        self.__connection_data = connection_data
        self.__client = None

    def connect(self, connection_data=None):
        if connection_data is not None:
            if not type(connection_data) is ConnectionData.ConnectionData:
                raise Exception('Wrong connection data type')
            self.__connection_data = connection_data
        self.__client = SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client.connect(hostname=self.__connection_data.get_host(),
                                   username=self.__connection_data.get_username(),
                                   password=self.__connection_data.get_password(),
                                   port=self.__connection_data.get_port())
        return CommandExecutor(self.__client)

    def get_cmd_executor(self):
        return CommandExecutor(self.__client)

    def get_connection_data(self):
        return self.__connection_data

    def set_connection_data(self, connection_data):
        if not type(connection_data) is ConnectionData.ConnectionData:
            raise Exception('Wrong connection data type')
        self.__connection_data = connection_data

