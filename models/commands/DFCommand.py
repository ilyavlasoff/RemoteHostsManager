from models.commands.Command import Command
from models.DTO.DFData import DFData


class DFCommand(Command):
    def __init__(self, ssh_client, params=None):
        if params is None:
            params = []
        params += ['h']
        command_text = 'df'
        super(DFCommand, self).__init__(ssh_client, command_text, [], params)

    def execute(self):
        data = super(DFCommand, self).execute()
        if 1:#try:
            df_data = DFCommand.__parse(data)
            if len(df_data) > 0:
                return df_data[1:]
        #except Exception:
        #    raise Exception('Error while parsing command')

    @staticmethod
    def __parse(data):
        df_lines = str.splitlines(str(data, 'utf-8'))
        df_items = []
        for line in df_lines:
            df_words = line.split()
            filesystem = df_words[0]
            size = df_words[1]
            used = df_words[2]
            avail = df_words[3]
            used_percent = df_words[4][:str.find('%', df_words[4])]
            mount_point = None if len(df_words) < 6 else df_words[5]
            item = DFData(filesystem, size, used, avail, used_percent, mount_point)
            df_items.append(item)
        return df_items
