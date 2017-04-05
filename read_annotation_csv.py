import csv
# with open('annotations_subset.csv',newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#

filename = "annotations_final.csv"
#TODO : dssign a function to sum up the tag count to find out popular tags





def get_table():
    f = open(filename, 'r')
    csv_cursor = csv.reader(f, delimiter='\t')

    table = []
    for row in csv_cursor:
        table.append(row)
    f.close()
    return table

def get_dict():
    f = open(filename, 'r')
    dict = csv.DictReader(f, delimiter='\t')
    return dict


def get_tags(table):
    return table[0]

# def tag_count(table, tag):
#     count = 0
#
#     for element in table:
#         #print(row[tag])
#         if element[tag] == '1' :
#             count+=1
#     print(count)
#     return count

def tag_count(table, tags):
    tt = list(map(list, zip(*table)))
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

#TODO : out put subset of annotation data with tags we picked