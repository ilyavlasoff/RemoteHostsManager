from models.commands.Command import Command
from models.DTO.LSData import LSData
import re
from dateutil import parser


class LSCommand(Command):
    def __init__(self, ssh_client, path, params=None):
        if params is None:
            params = []
        params += ['a', 'l', 'Q', 'h', 'full-time', 'A']
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
            try:
                filename = re.search(r'\".+\"|$', line).group().replace('"', '')
                if not filename:
                    continue
                datetime_str = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{9} [+-]\d{4}|$', line).group()
                datetime_value = parser.parse(datetime_str)
                data = line.split()

                def safe_indexing(index):
                    try:
                        value = data[index]
                    except IndexError:
                        value = 'Undefined'
                    return value

                ls_data_objects.append(LSData(safe_indexing(0), safe_indexing(2), safe_indexing(3),
                                              safe_indexing(4), datetime_value.strftime('%Y/%m/%d %H:%M'), filename))
            except Exception:
                pass
        return ls_data_objects
