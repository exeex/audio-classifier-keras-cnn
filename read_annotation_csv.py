import csv
# with open('annotations_subset.csv',newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#

filename = "annotations_final.csv"
#DONE : dssign a function to sum up the tag count to find out popular tags


def get_table():
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


def get_hot_tags():
    t = get_table()
    tags = get_tags(t)
    counts = tag_count(t,tags)
    return sorted(counts,key =lambda x:x[1] , reverse = True)



#TODO : design a function to pick some tag

def get_dict():
    f = open(filename, 'r')
    dict = csv.DictReader(f, delimiter='\t')
    return dict

def write_csv_subset(filename= "annotations_subset.csv" , tags=[]):
    d = get_dict()
    with open(filename, 'w') as csvfile:
        fieldnames = []
        fieldnames.append("clip_id")
        for tag in tags:
            fieldnames.append(tag)
        fieldnames.append("mp3_path")

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)




        writer.writeheader()
        writer.writerow({'clip_id': '0'})
        writer.writerow({'clip_id': '1'})
        writer.writerow({'clip_id': '2'})



table = get_table()
tt = transpose_table(table)
tags = get_tags(table)

for row in tt[0] :
    if row[0] not in tags:




    #   TODO : out put subset of annotation data with tags we picked

