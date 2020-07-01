
import yaml
import sys

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

def create_instance(instance, solution, solution_file_name):

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

        with open(solution) as f:
            solution = yaml.load( f, Loader=yaml.FullLoader )
        if not solution is None:
            itemkinds = []
            ids = []
            for i in solution['layout']['containers'][0]['loadingspaces'][0]['placements']:
                if i['itemid'] in ids:
                    itemkinds[ids.index(i['itemid'])]["quantity"] += 1
                    itemkinds[ids.index(i['itemid'])]["placed"] += 1
                    itemkinds[ids.index(i['itemid'])]["positions"].append(i["position"])
                    itemkinds[ids.index(i['itemid'])]["given_orientation"].append(i["orientation"])
                else:
                    ids.append(i['itemid'])
                    temp_block_dict = {}
                    temp_block_dict["id"] = i['itemid']
                    temp_block_dict["quantity"] = 1
                    temp_block_dict["placed"] = 1
                    temp_block_dict["positions"] = [i["position"]]
                    temp_block_dict["given_orientation"] = [i["orientation"]]
                    temp_block_dict["support"] = 1.0
                    temp_block_dict["color"] = i['color']
                    #only possible orientation is to place facing upwards like it was created
                    temp_block_dict["orientations"] = instance['data']['itemkinds'][i['itemid']-1]['orientations']
                    temp_block_dict["size"] = {}
                    temp_block_dict["size"]["width"] = instance['data']['itemkinds'][i['itemid']-1]['size']["width"]
                    temp_block_dict["size"]["length"] = instance['data']['itemkinds'][i['itemid']-1]['size']["length"]
                    temp_block_dict["size"]["height"] = instance['data']['itemkinds'][i['itemid']-1]['size']["height"]
                    itemkinds.append(temp_block_dict)
            for i in solution['layout']['unplaced']:
                if i['itemid'] in ids:
                    itemkinds[ids.index(i['itemid'])]["quantity"] += i["quantity"]
                else:
                    ids.append(i['itemid'])
                    temp_block_dict = {}
                    temp_block_dict["id"] = i['itemid']
                    temp_block_dict["quantity"] = i["quantity"]
                    temp_block_dict["placed"] = 0
                    temp_block_dict["support"] = 1.0
                    temp_block_dict["color"] = instance['data']['itemkinds'][i['itemid']-1]['color']
                    #only possible orientation is to place facing upwards like it was created
                    temp_block_dict["orientations"] = instance['data']['itemkinds'][i['itemid']-1]['orientations']
                    temp_block_dict["size"] = {}
                    temp_block_dict["size"]["width"] = instance['data']['itemkinds'][i['itemid']-1]['size']["width"]
                    temp_block_dict["size"]["length"] = instance['data']['itemkinds'][i['itemid']-1]['size']["length"]
                    temp_block_dict["size"]["height"] = instance['data']['itemkinds'][i['itemid']-1]['size']["height"]
                    itemkinds.append(temp_block_dict)



            container["itemkinds"] = itemkinds
            skeleton['data'] = container

        with open(solution_file_name, 'w') as file:
            documents = yaml.dump(skeleton, file)
        file.close()



def parse_args():
    if sys.argv == []:
        exit()
    return sys.argv[1], sys.argv[2], sys.argv[3]


if __name__ == "__main__":
    create_instance(*parse_args())
