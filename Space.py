class Space:
    def __init__(self, corner, size, kind):
        self.corner = corner
        self.size = size
        self.kind = kind

    def get_corner(self):
        return self.corner

    def get_size(self):
        return self.size

    def get_kind(self):
        return self.kind

    def __repr__(self):
        return "Space{%s,%s," % (self.corner, self.size) + self.kind + "}"
