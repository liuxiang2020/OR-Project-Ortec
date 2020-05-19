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
    
    def update_size_x(self, x):
        self.size[0] = x
        
    def update_size_y(self, y):
        self.size[1] = y
        
    def set_size(self, size):
        self.size = size
    
    def __repr__(self):
        return "Space{corner: %s, size: %s," % (self.corner, self.size,) + self.kind + "}\n"
