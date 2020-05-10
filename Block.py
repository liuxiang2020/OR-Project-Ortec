class Block:
    def __init__(self, block_id):
        self.id = block_id
        self.quantity = 0
        self.volume = 0
        self.size = 0
        self.orientation = 0
        self.fitness = 0

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

    def get_fitness(self):
        return self.fitness

    def set_item_quantity(self, quantity):
        self.quantity = quantity

    def set_size(self, size):
        self.size = size

    def set_orientation(self, orientation):
        self.orientation = orientation

    def set_volume(self, volume):
        self.volume = volume

    def set_volume_loss(self, volume_loss):
        self.volume_loss = volume_loss

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __repr__(self):
        return "{id: %s\n, quantity:%s\n, volume: %s\n, size: %s\n, orientation:%s\n, fitness:%s\n, volumeloss:%s" \
               % (self.id, self.quantity, self.volume, self.size, self.orientation,self.fitness,self.volume_loss) + "}\n"
