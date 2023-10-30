from typing import Dict

input_eaai17 = open('eaai17_annotations.tsv')

set_pairs = set()
set_unrelated = set()

dict_eaai17_annotated_pairs: Dict = {}

for line in input_eaai17:
    tokens = line.strip().split('\t')
    if len(tokens) < 3:
        continue
    head_name = tokens[0]
    tail_name = tokens[1]
    predictions = tokens[2:]
    count_true = predictions.count('1')
    count_reverse = predictions.count('2')
    count_unrelated = predictions.count('3')
    if count_true > 1 and max(count_true, count_reverse, count_unrelated) == count_true:
        dict_eaai17_annotated_pairs[f"{head_name}\t{tail_name}"] = 1
    elif count_reverse > 1 and max(count_true, count_reverse, count_unrelated) == count_reverse:
        dict_eaai17_annotated_pairs[f"{tail_name}\t{head_name}"] = 1
    elif count_unrelated > 1 and max(count_true, count_reverse, count_unrelated) == count_unrelated:
        dict_eaai17_annotated_pairs[f"{head_name}\t{tail_name}"] = 0

input_eaai17.close()

input_heads_rate = open('predicted_heads_rate.csv')

dict_heads_rate: Dict = {}
# head_name, head, rate
for line in input_heads_rate:
    tokens = line.strip().split(',')
    head_name = tokens[0]
    head = tokens[1]
    rate = float(tokens[2])
    dict_heads_rate[head] = rate

input_heads_rate.close()

input_tails_rate = open('predicted_tails_rate.csv')

dict_tails_rate: Dict = {}
# tail_name, tail, rate
for line in input_tails_rate:
    tokens = line.strip().split(',')
    tail_name = tokens[0]
    tail = tokens[1]
    rate = float(tokens[2])
    dict_tails_rate[tail] = rate

input_tails_rate.close()

input_student_annotation_range = open('student_annotation_range.csv')

student_annotation_indices = set()
# index, annotation, head_name, tail_name, score, incidence, head, tail
for line in input_student_annotation_range:
    tokens = line.strip().split(',')
    index = int(tokens[0])
    student_annotation_indices.add(index)

input_student_annotation_range.close()

input_student_annotation = open('annotated_by_students.csv')
dict_student_annotated_pairs: Dict = {}

# index, annotation, head_name, tail_name, score, incidence, head, tail
for line in input_student_annotation:
    tokens = line.strip().split(',')
    index = tokens[0]
    annotation = tokens[1]
    head = tokens[6]
    tail = tokens[7]
    dict_student_annotated_pairs[f"{head}_{tail}"] = annotation


class Triple:
    def __init__(self, head, tail, head_name, tail_name, score, incidence, head_rate, tail_rate, annotation):
        self.head = head
        self.tail = tail
        self.head_name = head_name
        self.tail_name = tail_name
        self.score = score
        self.incidence = incidence
        self.head_rate = head_rate
        self.tail_rate = tail_rate
        self.labeled_class = annotation


dict_final_triples: Dict = {}

input_predicted = open('predicted_triples.csv')

# idx, head_name, "is_preceded_by", tail_name, score, incidence, head, tail
for line in input_predicted:
    tokens = line.strip().split(',')
    index = int(tokens[0])
    head_name = tokens[1]
    tail_name = tokens[3]
    score = float(tokens[4])
    if score < 0.5: # skip negative scores
        continue
    incidence = float(tokens[5])
    head = tokens[6]
    tail = tokens[7]
    if head in dict_heads_rate:
        head_rate = dict_heads_rate[head]
    else:
        head_rate = 0.0
    if tail in dict_tails_rate:
        tail_rate = dict_tails_rate[tail]
    else:
        tail_rate = 0.0
    labeled_class = -1
    # set student annotation range (~2356, 20794~ and included in indices) to false
    if index <= 2356 or index >= 20794:
        if index in student_annotation_indices:
            labeled_class = 0
    # student annotation
    if f"{head}_{tail}" in dict_student_annotated_pairs:
        # both students agreed
        if dict_student_annotated_pairs[f"{head}_{tail}"] == '2':
            labeled_class = 1
        else:  # two students disagreed; regard as not annotated
            labeled_class = -1
    # eaai17 annotation is more reliable than student annotation
    if f"{head_name}\t{tail_name}" in dict_eaai17_annotated_pairs:
        labeled_class = dict_eaai17_annotated_pairs[f"{head_name}\t{tail_name}"]
    dict_final_triples[f"{head}_{tail}"] = Triple(
        head, tail, head_name, tail_name, score, incidence, head_rate, tail_rate, labeled_class)

input_predicted.close()

output = open('annotated_predicted_triples.csv', 'w')
output.write(
    'triple_name,score,triple_incidence,head_rate,tail_rate,labeled_class\n')
for key in dict_final_triples.keys():
    triple: Triple = dict_final_triples[key]
    output.write(
        f"{triple.head_name}\t{triple.tail_name},{triple.score},{triple.incidence},{triple.head_rate},{triple.tail_rate},{triple.labeled_class}\n")
output.close()
