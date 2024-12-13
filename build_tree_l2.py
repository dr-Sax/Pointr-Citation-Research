from pedestrian_dead_reckoning import *
import json


if __name__=="__main__":
        # Load the JSON data from the file
    with open('patent_tree.json', 'r') as f:
        l2_data = json.load(f)

    with open('pointr_patent_tree_l1.json', 'r') as f:
        l1_data = json.load(f)

    L2_PATENTS_LIST = []

    for patent in l1_data.keys():
        L2_PATENTS_LIST += l1_data[patent]['forward_citations'] + l1_data[patent]['forward_family_citations'] + l1_data[patent]['backward_citations'] + l1_data[patent]['backward_family_citations']

    unique_l2_patents_list = list(set(L2_PATENTS_LIST)) 
    for patent in unique_l2_patents_list:
        print(patent)
        try:
            l2_data[patent] = json_builder(patent)
        except:
            print('failed')

    # Write the updated JSON data back to the file
    with open('data.json', 'w') as f:
        json.dump(l2_data, f, indent=4)  # indent for pretty formatting