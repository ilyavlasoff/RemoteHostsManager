from models.commands.Command import Command
from models.DTO.LSData import LSData


class LSCommand(Command):
    def __init__(self, ssh_client, path, params=None):
        if params is None:
            params = []
        params += ['a', 'l']
        command_text = 'ls'
        super(LSCommand, self).__init__(ssh_client, command_text, [path], params)

    def execute(self):
        data = super(LSCommand, self).execute()
        try:
            ls_objects = LSCommand.__parse(data)
            filtered_ls = list(filter(lambda v: v.name not in ['.', '..'], ls_objects))
            return filtered_ls
        except Exception:
            raise Exception('Error while parsing command response')

    @staticmethod
    def __parse(data):
        lines = str.splitlines(str(data, 'utf-8'))
        ls_data_objects = []
        for line in lines:
            data = line.split()
            try:
                ls_data_objects.append(LSData(data[0], data[2], data[3], data[4], ','.join(data[5:7]), data[8]))
            except Exception:
                pass
        return ls_data_objects
