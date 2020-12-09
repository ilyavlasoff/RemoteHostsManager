from models.commands import Command


class RMCommand(Command.Command):
    def __init__(self, ssh_client, delete_path, params=None):
        if params is None:
            params = []
        params += ['r', 'f']
        command_text = 'rm'
        super(RMCommand, self).__init__(ssh_client, command_text, [delete_path], params)

    def execute(self):
        try:
            super(RMCommand, self).execute()
        except Exception:
            raise Exception('Problem while removing item')
        return True

    @staticmethod
    def __parse(data):
        pass
