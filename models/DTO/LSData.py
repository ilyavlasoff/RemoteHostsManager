class LSData:
    def __init__(self, rights, creator, owner, size, created_at, name):
        self.type = rights[0]
        self.access_rights = rights
        self.creator = creator
        self.owner = owner
        self.size = size
        self.created_at = created_at
        self.name = name

    def is_dir(self):
        return self.type == 'd'

