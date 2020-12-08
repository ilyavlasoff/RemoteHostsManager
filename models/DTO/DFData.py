class DFData:
    def __init__(self, filesystem, size, used, avail, use_percent, mount_point):
        self.filesystem = filesystem
        self.size = size
        self.used = used
        self.avail = avail
        self.use_percent = use_percent
        self.mount_point = mount_point
