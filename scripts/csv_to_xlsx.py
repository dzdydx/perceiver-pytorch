# -*- coding: utf-8 -*-
# @Time    : 2021/11/10 11:17 AM
# @Author  : dzdydx
# @Affiliation  : 
# @Email   : 
# @File    : csv_to_xlsx.py

# =========================
#         Archived.
# =========================

import os
import xlsxwriter
from tqdm import tqdm

g = open('../dataset/eval-labels.csv').read()
h = g.split('\n')
ids = list()
starts = list()
ends = list()
classes = list()

for i in tqdm(range(len(h)), desc='reading data'):
    try:
        temp = h[i].split(', ')
        # print(temp)
        ids.append(temp[0])
        starts.append(temp[1])
        ends.append(temp[2])
        classes.append(temp[3])
    except:
        pass

# now make a dataframe
workbook = xlsxwriter.Workbook('eval_segments.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Ids')
worksheet.write('B1', 'Start')
worksheet.write('C1', 'End')
worksheet.write('D1', 'Classes')

print(len(ids), len(starts), len(ends), len(classes))

for i in tqdm(range(len(ids) - 1), desc='writing excelsheet'):
    worksheet.write('A%s' % (str(i+2)), ids[i])
    worksheet.write('B%s' % (str(i+2)), starts[i])
    worksheet.write('C%s' % (str(i+2)), ends[i])
    worksheet.write('D%s' % (str(i+2)), classes[i])

workbook.close()
