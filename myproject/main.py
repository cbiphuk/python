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

report = []

def Income(report):
    for item in report:
        if float(item[2]) > 0:
            item.append("INCOME")

def ExcludeList(report):
    for item in report:
        if item[1].find('Check') != -1 and (float(item[2]) == -156.25 or float(item[2]) == -2000):
            item.append("EXCLUDE")
            #print item
        if item[1].find('AT&T*BILL') != -1  or item[1].find('VERIZON*ONETIMEPAY') != -1  or item[1].find('PSE&G-NJ') != -1:
            item.append("EXCLUDE")

def Other(report):
    for item in report:
        if item.__len__() < 4:
            item.append("OTHER")

def Sorting2(expense_list, expense_type):
    for item in expense_list:
        for expense_type_id in expense_type:
            for expense_name in expense_type[expense_type_id]:
                if item[1].find(expense_name) != -1:
                    item.append(expense_type_id)
                    #print item

def ReportLoader(file_name,report):
    try:
        bank_report = open(file_name)
    except:
        sys.exit("ERROR OPENING FILE")

    for line in bank_report.read().splitlines():
        if line[0] == 'D':
            date = line[1:]
        elif line[0] == 'P':
            description = line[1:]
        elif line[0] == 'T':
            value = line[1:]
        elif line[0] == '^':
            report.append([date,description,value])

def PrintReport(report):
    for item in report:
        print item

def PrintReport2(report, filters):
    for item in report:
        if item[3] == filters:
            print item
        elif filters == "":
            print item

def PeriodLen(report):
    print report[0]

def SpendsByType(report):
    spends = {}
    for report_elem in report:
        
        if report_elem[3] not in spends.keys():
            #print '%s not in %s' %(report_elem[3], spends.keys())
            #print i[3]
            spends[report_elem[3]] = 1
            #print spends
        else:
            spends[report_elem[3]] += 1
            #print 'else'
    print spends

ReportLoader("stmt_y4.qif_",report)
Sorting2(report,filters)
Income(report)
ExcludeList(report)
Other(report)
#PrintReport(report)
#PrintReport2(report,"EXCLUDE")
#PrintReport2(report,"EXCLUDE")
#PeriodLen(report)
SpendsByType(report)
"""
sum = 0
print type(sum)    
for item in report:
    if item[3] != 'EXCLUDE' and item[3] != 'INCOME':
        print item
        sum += float(item[2])


print sum/29
"""




