from pedestrian_dead_reckoning import *
import json


if __name__=="__main__":
        # Load the JSON data from the file
    with open('patent_tree.json', 'r') as f:
        data = json.load(f)

    for patent in POINTR_PATENTS_LIST:
        data[patent] = json_builder(patent)

    # Write the updated JSON data back to the file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)  # indent for pretty formatting