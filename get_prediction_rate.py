from typing import Dict

f = open('predicted_triples.csv')
lines = f.readlines()
f.close()

count_heads: Dict = {}
count_tails: Dict = {}
entity_map: Dict = {}

for line in lines:
    tokens = line.strip().split(',')
    head_name = tokens[1]
    tail_name = tokens[3]
    head = tokens[6]
    tail = tokens[7]
    if head not in entity_map:
        entity_map[head] = head_name
    if tail not in entity_map:
        entity_map[tail] = tail_name
    if head not in count_heads:
        count_heads[head] = 0
    if head not in count_tails:
        count_tails[head] = 0
    if tail not in count_heads:
        count_heads[tail] = 0
    if tail not in count_tails:
        count_tails[tail] = 0
    count_heads[head] += 1
    count_tails[tail] += 1

sum_count = len(lines)

out_heads = open('predicted_heads_rate.csv', 'w')
out_tails = open('predicted_tails_rate.csv', 'w')

for key in count_heads.keys():
    out_heads.write(entity_map[key] + ',' + key + ',' + str(count_heads[key] / sum_count) + '\n')
    out_tails.write(entity_map[key] + ',' + key + ',' + str(count_tails[key] / sum_count) + '\n')

out_heads.close() 
out_tails.close()