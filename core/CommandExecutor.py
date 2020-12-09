from models.commands import LSCommand, DFCommand, RMCommand, MVCommand


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
