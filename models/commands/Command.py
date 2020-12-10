class Command:
    def __init__(self, ssh_client, command_text, command_args, params):
        self.command_args = ' '.join(command_args)
        self.params = ' '.join(['-%s' % param if len(param) == 1 else '--%s' % param for param in params])
        self.client = ssh_client
        self.command_text = command_text

    def execute(self):
        stdin, stdout, stderr = self.client.exec_command('%s %s %s' % (self.command_text, self.params, self.command_args))
        return stdout.read() + stderr.read()

    @staticmethod
    def __parse(data):
        raise NotImplementedError()