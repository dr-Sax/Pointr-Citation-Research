import json

with open('formatted_patent_data/l1_l2_mix_tree_fmt.json', 'r') as f:
    data = json.load(f)

companies = []

for patent in data['nodes']:
    companies.append(patent['company'])

print(list(set(companies)))