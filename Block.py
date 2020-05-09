class Block:
    def __init__(self, block_id):
        self.id = block_id
    
    def get_id(self):
        return self.id

    def get_item_quantity(self):
        return self.quantity
    
    def get_size(self):
        return self.size

    def get_orientation(self):
        return self.orientation

    def get_volume(self):
        return self.volume
    
    def get_volume_loss(self):
        return self.volume_loss

    def set_item_quantity(self, quantity):
        self.quantity = quantity
    
    def set_size(self, size):
        self.size = size

    def set_orientation(self, orientation):
        self.orientation = orientation

    def set_volume(self, length, width, height):
        self.volume = length* width* height

    def set_volume_loss(self, volume_loss):
        self.volume_loss = volume_loss

    def __repr__(self):
        return "{id: %d\n, quantity:%d\n, volume: %d\n, size: %s\n, orientation:%s" \
               % (self.id , self.quantity, self.volume, self.size, self.orientation )+"}\n"