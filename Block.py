"""
Class Block :
- block_ids: a list of blocks (We give each block an id) eg. [Block A, Block B]
- id_quantity: a dictionary consist of id and its corresponding quantity eg. {id: quantity, id:quantity}
- size: block size, a list of [L,W,H] eg. [100, 40, 100]
- orientation:
- fitness:
"""

class Block:
    def __init__(self, id_quantity, simple_block=False):
        #self.id = block_id
        self.id_quantity = id_quantity
        self.volume = 0
        self.size = 0
        self.fitness = 0
        self.is_simple_block = simple_block

    def get_unique_id(self):
        return self.unique_id

    def get_block_uids(self):
        return self.block_uids    

    def get_id_quantity(self):
        return self.id_quantity
    
    def get_is_simple_block(self):
        return self.is_simple_block

    def get_upper_face(self):
        return self.upper_face

    def get_added_direction(self):
        return self.added_direction

    def get_dr_quantity(self):
        return self.dr_quantity

    def get_item_quantity(self):
        return self.quantity

    def get_size(self):
        return self.size

    def get_volume(self):
        return self.volume

    def get_volume_loss(self):
        return self.volume_loss

    def get_fitness(self):
        return self.fitness

    def set_block_uids(self, block_uids):
        self.block_uids = block_uids    

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id
    
    def set_upper_face(self,upper_face):
        self.upper_face = upper_face
    
    def set_added_direction(self,added_direction):
        self.added_direction = added_direction
        
    def set_id_quantity(self, id_quantity):
        self.id_quantity = id_quantity
    
    def set_dr_quantity(self, dr_quantity):
        self.dr_quantity = dr_quantity

    def set_size(self, size):
        self.size = size

    def set_volume(self, volume):
        self.volume = volume

    def set_volume_loss(self, volume_loss):
        self.volume_loss = volume_loss

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __repr__(self):
        return "{id_quantity: %s\n, volume: %s\n, size: %s\n, fitness:%s\n, volumeloss:%s" \
               % (self.id_quantity, self.volume, self.size,self.fitness,self.volume_loss) + "}\n"
