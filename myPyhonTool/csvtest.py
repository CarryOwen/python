import csv
list1=[1,2,3,4]
f = open('csvtest.csv','a',encoding='utf-8',newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(list1)
f.close()