from models.commands.Command import Command


class MVCommand(Command):
    def __init__(self, ssh_client, source_path, destination_path, params=None):
        if params is None:
            params = []
        command_text = 'mv'
        super(MVCommand, self).__init__(ssh_client, command_text, [source_path, destination_path], params)

    def execute(self):
        try:
            super(MVCommand, self).execute()
        except Exception:
            raise Exception('Problem while executing command')

    @staticmethod
    def __parse(data):
        pass
