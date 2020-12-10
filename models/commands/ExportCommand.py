import os


class ExportCommand:
    def __init__(self, ssh_client, local_path, remote_path, del_local=True):
        self.sftp_client = ssh_client.open_sftp()
        self.local_path = local_path
        self.remote_path = remote_path
        self.del_local = del_local

    def execute(self):
        if not os.path.exists(self.local_path):
            raise Exception('Local file not exists')
        try:
            self.sftp_client.put(self.local_path, self.remote_path)
        except Exception:
            raise Exception('File can not be downloaded')
