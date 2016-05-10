#!/usr/bin/env python

import sys

food = ('STARBUCKS','THINK COFFEE','KOBRICK COFFEE','MCDONALD')

filters = {'KABAKI':('STARBUCKS','THINK COFFEE','KOBRICK COFFEE','MCDONALD'),\
        'COSMETICS':('LASH FOREVER','SEPHORA',"MACY'S"),\
        'PHARMACY':('Duane Reade','additional123123123123123123123123123123123123'),\
        'CLOTHES':('GAP US','PARAGON ATHLETIC','JCPENNEY'),\
        'FOOD':('ACME','123121351412412123'),
        'CRAP':('KEEP THE CHANGE TRANSFER','1241214124')\
        }


def Sorting(expense_list, expense_type):
    for item in expense_list:
        for expense_type_id in expense_type:
            if item[1].find(expense_type_id) != -1:
                item.append("FOOD")

def Sorting2(expense_list, expense_type):
    for item in expense_list:
        for expense_type_id in expense_type:
            for expense_name in expense_type[expense_type_id]:
                if item[1].find(expense_name) != -1:
                    item.append(expense_type_id)
                    print item

try:
    bank_report = open("stmt_y4.qif_")
except:
    sys.exit("ERROR OPENING FILE")

report = []

for line in bank_report.read().splitlines():
    if line[0] == 'D':
        date = line[1:]
    elif line[0] == 'P':
        description = line[1:]
    elif line[0] == 'T':
        value = line[1:]
    elif line[0] == '^':
        report.append([date,description,value])

#Sorting(report,food)
Sorting2(report,filters)


summ = 0
for item in report:
    
    if item.__len__() > 3:
        if item[3] == "FOOD":
            summ += float(item[2])
        

#for line in report:
#    print line
print "==================================================================="
for line in report:
    if line.__len__() == 3:
        print line
