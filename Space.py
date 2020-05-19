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
    
    def update_size_x(self, x):
        self.size[0] = x
        
    def update_size_y(self, y):
        self.size[1] = y
        
    def set_size(self, size):
        self.size = size
    
    def __repr__(self):
        return "Space{corner: %s, size: %s, block_corner: %s," % (self.corner, self.size, self.block_corner) + self.kind + "}\n"
