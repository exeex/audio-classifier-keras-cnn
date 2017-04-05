import csv
# with open('annotations_subset.csv',newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#


#DONE : dssign a function to sum up the tag count to find out popular tags


def get_table(filename = "annotations_final.csv"):
    f = open(filename, 'r')
    csv_cursor = csv.reader(f, delimiter='\t')

    table = []
    for row in csv_cursor:
        table.append(row)
    f.close()
    return table


def get_tags(table):
    return table[0]

def transpose_table(table):
    return list(map(list, zip(*table)))

def tag_count(table, tags):
    tt = transpose_table(table)
    counts=[]
    for x in range(1,len(tt)):
        counts.append([tags[x],tt[x].count('1')])
    return counts


def get_hot_tags(top_n = 10):
    t = get_table()
    tags = get_tags(t)
    counts = tag_count(t,tags)
    tag_rank = sorted(counts, key=lambda x: x[1], reverse=True)
    new_tags =[]
    for element in tag_rank[0:top_n]:
        new_tags.append(element[0])
    return new_tags



#TODO : design a function to pick some tag

def get_dict():
    f = open(filename, 'r')
    dict = csv.DictReader(f, delimiter='\t')
    return dict

def write_csv_subset(table,filename= "annotations_subset.csv" , tags=[]):
    get_table_subset(table, tags)
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for row in table:
            writer.writerow(row)

def get_table_subset(table,tags):
    #table = get_table()
    #tags = get_hot_tags()
    tt = transpose_table(table)
    new_tt = []
    new_tt.append(tt[0])
    for row in tt:
        if row[0] in tags:
            new_tt.append(row)
    new_tt.append(tt[-1])
    return transpose_table(new_tt)

table = get_table()
tags = get_hot_tags()
write_csv_subset(table,filename= "annotations_subset.csv" ,tags=tags)

#TODO : out put subset of annotation data with tags we picked

