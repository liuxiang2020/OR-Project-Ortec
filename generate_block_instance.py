from Block import *
from Functions import *
from config import *
import yaml

def SkeletonInstance():
    skeleton = """description:
  set: Bischoff & Ratcliff
  name: '1.1'
constraints:
- name: orientation
- name: support
objectives:
- name: average_fill_rate
  weight: 1.0
  priority: 1
- name: item_count
  weight: 1.0
  priority: 2"""
    return yaml.load( skeleton, Loader=yaml.FullLoader )

def create_instance(instance, state, solution_file_name):

    #some hardcoded colors
    COLORS = ['#029E73','#0173B2','#0233B2','#0333B2','#0433B2','#0533B2','#0633B2','#0733B2','#0833B2','#0933B2','#1111B2','#1222B2','#1333B2','#1444B2','#1555B2','#1666B2','#1777B2','#1888B2']
    UNPLACED_COLOR = '#111111'

    skeleton = SkeletonInstance()
    with open(instance) as f:
        instance = yaml.load( f, Loader=yaml.FullLoader )
    if not instance is None:
        container = {}
        palletkinds = []
        container["palletkinds"] = palletkinds
        boxkinds = []
        container["boxkinds"] = boxkinds
        containerkinds = []
        c = {}
        c["id"] = 1
        c["quantity"] = 1
        c["loadingspaces"] = []
        l = {}
        l["id"] = 1
        l["position"] = "0,0,0"
        l["size"] = {}
        l["size"]["length"] = instance['data']["containerkinds"][0]["loadingspaces"][0]["size"]["length"]
        l["size"]["width"] = instance['data']["containerkinds"][0]["loadingspaces"][0]["size"]["width"]
        l["size"]["height"] = instance['data']["containerkinds"][0]["loadingspaces"][0]["size"]["height"]
        c["loadingspaces"].append(l)
        containerkinds.append(c)
        container["containerkinds"] = containerkinds

        itemkinds = []
        blocks = state.get_planListBlock()
        id = 0
        for i in range(len(blocks)):
            #enter placed blocks in the list
            cur_block = blocks[id]
            temp_block_dict = {}
            temp_block_dict["id"] = id
            temp_block_dict["quantity"] = 1
            temp_block_dict["support"] = 1.0
            temp_block_dict["color"] = COLORS[id]
            #only possible orientation is to place facing upwards like it was created
            temp_block_dict["orientations"] = "WLH"
            temp_block_dict["size"] = {}
            temp_block_dict["size"]["width"] = int(cur_block.get_size()[0])
            temp_block_dict["size"]["length"] = int(cur_block.get_size()[1])
            temp_block_dict["size"]["height"] = int(cur_block.get_size()[2])
            itemkinds.append(temp_block_dict)
            id += 1


        # Adding unplaced boxes? Most of the time this will only result in an infeasible model which the excact method won't solve
        #enter unplaced boxes into list
        unplaced_items =  state.get_available_items()
        for item, quan in unplaced_items.items():
            if(quan > 0):
                temp_box_dict = {}
                temp_box_dict["id"] = id
                temp_box_dict["quantity"] = quan
                temp_box_dict["support"] = 1.0
                temp_box_dict["color"] = UNPLACED_COLOR
                temp_box_dict["orientations"] = instance['data']["itemkinds"][item - 1]["orientations"]
                temp_box_dict["size"] = {}
                temp_box_dict["size"]["width"] = instance['data']["itemkinds"][item - 1]["size"]["width"]
                temp_box_dict["size"]["length"] = instance['data']["itemkinds"][item - 1]["size"]["length"]
                temp_box_dict["size"]["height"] = instance['data']["itemkinds"][item - 1]["size"]["height"]
                itemkinds.append(temp_box_dict)
                id += 1


        container["itemkinds"] = itemkinds
        skeleton['data'] = container

    with open(solution_file_name, 'w') as file:
        documents = yaml.dump(skeleton, file)
    file.close()
