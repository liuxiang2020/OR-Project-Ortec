class Space:
    def __init__(self, corner, size, kind, block_corner):
        self.corner = corner
        self.size = size
        self.kind = kind
        self.block_corner = block_corner

    def get_corner(self):
        return self.corner

    def get_size(self):
        return self.size

    def get_kind(self):
        return self.kind

    def get_block_corner(self):
        return self.block_corner
    
    def __repr__(self):
        return "Space{corner: %s, size: %s, block_corner: %s," % (self.corner, self.size, self.block_corner) + self.kind + "}\n"
