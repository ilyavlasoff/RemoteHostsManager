import os


class ImportCommand:
    def __init__(self, ssh_client, remote_path, local_path, del_remote):
        self.sftp_client = ssh_client.open_sftp()
        self.remote_path = remote_path
        self.local_path = local_path
        self.del_remote = del_remote

    def execute(self):
        try:
            self.sftp_client.get(self.remote_path, self.local_path)
        except Exception:
            raise Exception('File can not be downloaded')

