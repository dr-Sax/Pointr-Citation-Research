# file to get patent json in form for node visualization

import json

if __name__=="__main__":
    # Load in raw patent data:
    with open('raw_patent_data/pointr_patent_tree_l1_l2_mix.json', 'r') as f:
        data = json.load(f)
        # fmt for network graph visualization:
        node_fmt = {
            "nodes":[],
            "links":[] 
        }
        node_size = {}
    
    with open('raw_patent_data/img_urls.json', 'r') as f:
        imgUrls = json.load(f)

    for key in data:
        if {'id': key} not in node_fmt['nodes']:  # checks for duplicate
            node_fmt["nodes"].append({"id": key})
            node_size[key] = 1
        else:
            node_size[key] = node_size[key] + 1
            
        t = data[key]['forward_citations'] + data[key]['forward_family_citations']
        s = data[key]['backward_citations'] + data[key]['backward_family_citations']
        
        if data[key]['assignee'] == "Pointr Ltd":
            for c in t:
                if {'id': c} not in node_fmt['nodes']: # checks for duplicate
                    node_fmt["nodes"].append({"id": c})
                    node_size[c] = 1
                else:
                    node_size[c] = node_size[c] + 1
                node_fmt["links"].append({"source": c,"target": key})
            for c in s:
                if {'id': c} not in node_fmt['nodes']: # checks for duplicate
                    node_fmt["nodes"].append({"id": c})
                    node_size[c] = 1
                else:
                    node_size[c] = node_size[c] + 1
                node_fmt["links"].append({"source": key, "target": c})
    

    node_sizes = []
    for key in node_size.keys():
        try:
            title = data[key]['title']
            company = data[key]['assignee']
            pubdate = data[key]['pubdate']
            try:
                img_url = imgUrls[company]
            except:
                img_url = ''
            node_sizes.append({"id": key, "size": 1000 * (node_size[key]), "title": title, "company": company, "pubdate": pubdate, "imgurl": img_url})
        except: # level 2 items which dont have details on title, author, etc.
            node_sizes.append({"id": key, "size": 1000 * (node_size[key]), "title": "", "company": "", "pubdate": "", "imgurl":""})

        
    
    node_fmt["nodes"] = node_sizes
    # # Write the updated JSON data back to the file
    with open('l1_l2_mix_tree_fmt.json', 'w') as f:
         json.dump(node_fmt, f, indent=4)  # indent for pretty formatting

 