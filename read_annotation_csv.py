import csv
import numpy as np
import random
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
    return table[0][1:-1]

def get_fieldnames(table):
    return table[0]

def transpose_table(table):
    return list(map(list, zip(*table)))

def tag_count(table, tags):
    tt = transpose_table(table)
    counts=[]
    for x in range(1,len(tt)-1):
        counts.append([tags[x],tt[x].count('1')])
    return counts


def get_hot_tags(top_n = 10):
    t = get_table()
    #tags = get_tags(t)
    tags = get_fieldnames(t)
    counts = tag_count(t,tags)
    tag_rank = sorted(counts, key=lambda x: x[1], reverse=True)
    new_tags =[]
    for element in tag_rank[0:top_n+1]:
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
        writer = csv.writer(csvfile, delimiter='\t',lineterminator='\r')
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

def build_subset_csv():
    table = get_table()
    tags = get_hot_tags(50)
    table2 = get_table_subset(table,tags)
    write_csv_subset(table2,filename= "annotations_subset.csv" ,tags=tags)

#TODO : out put subset of annotation data with tags we picked

#def get_file_path
#def get_tag_vector


class Csv_parser :
    def __init__(self , filename = "annotations_subset.csv"):
        table = get_table(filename)
        self.table_content = table[1:]
        self.tags = get_tags(table)
    def get_file_path(self,idx):
        return self.table_content[idx][-1]
    def get_tag_vector(self,idx):
        return self.table_content[idx][1:-1]
    def get_clip_number(self,idx):
        return self.table_content[idx][0]
    def get_table(self):
        return self.table_content
    def get_tags(self):
        return self.tags
    def get_total_files(self):
        tt = transpose_table(self.table_content)
        return tt[-1]
    def get_tag_np_vector(self,idx):
        v = self.get_tag_vector(idx)
        v2 = np.zeros(len(self.tags))
        try:
            for idx , value in enumerate(v):
                if v[idx] == '1':
                    v2[idx] = 1
            return v2

        except:
            return None
    def get_file_numbers(self):
        return len(self.table_content)

    def subset(self, percentage):
        total = self.get_file_numbers()
        partial = int(round(total*percentage,0))
        self.table_content = self.table_content[0:partial]

    def shuffle(self):
        random.shuffle(self.table_content)


csv_content = Csv_parser()