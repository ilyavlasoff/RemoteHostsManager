from models.commands import LSCommand, DFCommand, RMCommand, MVCommand, ImportCommand, ExportCommand


class CommandExecutor:
    def __init__(self, ssh_client):
        self.client = ssh_client

    def get_ls_command(self, destination_path=None):
        if destination_path is None:
            destination_path = '/'
        return LSCommand.LSCommand(self.client, destination_path)

    def get_df_command(self):
        return DFCommand.DFCommand(self.client)

    def get_rm_command(self, remove_path):
        return RMCommand.RMCommand(self.client, remove_path)

    def get_mv_command(self, source, destination):
        return MVCommand.MVCommand(self.client, source, destination)

    def get_import_command(self, remote_path, local_path, del_remote):
        return ImportCommand.ImportCommand(self.client, remote_path, local_path, del_remote)

    def get_export_command(self, local_path, remote_path):
        return ExportCommand.ExportCommand(self.client, local_path, remote_path)
