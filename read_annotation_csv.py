import csv
# with open('annotations_subset.csv',newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
#

filename = "annotations_final.csv"
f = open(filename, 'r')

#TODO : dssign a function to sum up the tag count to find out popular tags

def get_tags(f):
    for idx , row in enumerate(csv.reader(f,delimiter='\t')):
        if idx ==0 :
            print(row)

def tag_count(file = f, tag = "no voice"):
    count = 0
    for row in csv.DictReader(file,delimiter='\t'):
        #print(row[tag])
        if row[tag] == '1' :
            count+=1

    print(count)




#TODO : design a function to pick some tag

#TODO : out put subset of annotation data with tags we picked