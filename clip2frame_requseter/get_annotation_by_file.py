
from clip2frame_requseter.request_json import request_json




import csv
filename = "fileurls.csv"

def get_table():
    f = open(filename, 'r')
    csv_cursor = csv.reader(f)

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


table = get_table()
tt = transpose_table(table)
tags = get_tags(table)



urls = tt[3][1:]
songname = tt[1][1:]

data = []
urls = urls[0:1]



for url in urls:
    data.append(request_json(url))
    print("!")
