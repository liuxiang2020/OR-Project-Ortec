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
        self.real_volume = 0
        self.absolute_volume = 0
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

    def get_real_volume(self):
        return self.real_volume

    def get_absolute_volume(self):
        return self.absolute_volume

    def get_volume_loss(self):
        return (self.absolute_volume - self.real_volume)

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

    def set_absolute_volume(self, absolute_volume):
        self.absolute_volume = absolute_volume
        
    def set_real_volume(self, real_volume):
        self.real_volume = real_volume        

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __repr__(self):
        return "{id_quantity: %s\n, absolute_volume: %s\n, real_volume: %s\n, size: %s\n, fitness:%s\n, volumeloss:%s" \
               % (self.id_quantity, self.absolute_volume, self. real_volume, self.size,self.fitness, self.get_volume_loss()) + "}\n"
