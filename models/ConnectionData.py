class ConnectionData:
    def __init__(self, host=None, username=None, password=None, port=22, id=None):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__port = port
        self.__id = id

    def set_host(self, host):
        self.__host = host

    def get_host(self):
        return self.__host

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_port(self, port):
        self.__port = port

    def get_port(self):
        return self.__port

    def get_connection_string(self):
        return '%s@%s' % (self.__username, self.__host)

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
