#Code to calculate TF-IDF value:

from scipy import spatial
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
from collections import Counter
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
document = "aa bb cc"
query="aa dd"
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([document,query])
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
x=1-spatial.distance.cosine(denselist[0],denselist[1])
print(x)

from scipy import spatial
from sklearn.feature_extraction.text import TfidfVectorizer
from google.colab import auth
auth.authenticate_user()
import re
import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())
worksh = gc.open('Output-TF-IDF').sheet1
worksheet = gc.open('HIPAA-Clauses').get_worksheet(0)

# get_all_values gives a list of rows:
rows = worksheet.get_all_values()

from math import*
#function to calculate the tf-idf:
def tfidf(document, query):
  vectorizer = TfidfVectorizer()
  vectors = vectorizer.fit_transform([document,query])
  feature_names = vectorizer.get_feature_names()
  dense = vectors.todense()
  denselist = dense.tolist()
  x=1-spatial.distance.cosine(denselist[0],denselist[1])
  return x
#
workshe = gc.open('HIPAA-Clauses').get_worksheet(1)
raid=[]
brid=[]
cids=[]
#get_all_values gives a list of rowss:
rowsss = workshe.get_all_values()

for i in range(1,201):
  if rowsss[i][0]!="":
    raid.append(rowsss[i][0])
    brid.append(rowsss[i][1])
worksh = gc.open('Output-TF-IDF').sheet1
works = gc.open('HIPAA-Clauses').get_worksheet(2)
rowss = works.get_all_values()

work = gc.open('breach_reports').sheet1
row = work.get_all_values()
j=1
num=2
numb=0
pn=1
recall=0
reca=0
prec=0
precision=0
#for loop to go through all the resolution agreements:
for i in range(0,len(brid)):
  r = re.sub("", " ",  brid[i]).split()
  if len(r)<3:
    text=rowss[j][2]
    print(j)
    j=j+1
    if j>33:
      break
  else:
    text=row[int(brid[i])-1][8]
#

  data = []
  ids=[]
  indices=[]

  for i in range (1,59):
    policy=rows[i][2]
    id=rows[i][0]
    data.append(str(id)+" "+str(tfidf(policy,text)))

  for i in range(0,58):
    r = re.sub(" ", " ",  data[i]).split()
    ids.append(r[0])
    indices.append(r[1])
  

# using bubblesort algorithm:
  def bubbleSort(list1):  
    # Outer loop for traverse the entire list  
    for i in range(0,len(list1)-1):  
        for j in range(len(list1)-1):  
            if(list1[j]<list1[j+1]):  
                temp = list1[j]  
                list1[j] = list1[j+1]  
                list1[j+1] = temp
                temp = ids[j]  
                ids[j] = ids[j+1]  
                ids[j+1] = temp
      
  bubbleSort(indices)
#updating the excel sheet as per the outputs:
  cell_list = worksh.range('A'+str(num-1)+':A'+str(num-1))
  for cell in cell_list:
    cell.value = raid[numb]
  numb=numb+1
  worksh.update_cells(cell_list)
  idn=0
  for n in range(num,num+58):  
    cell_list = worksh.range('A'+str(n)+':A'+str(n))
    for cell in cell_list:
      cell.value = ids[idn]
    worksh.update_cells(cell_list)
    idn=idn+1
  idn=0
  for n in range(num,num+58):  
    cell_list = worksh.range('B'+str(n)+':B'+str(n))
    for cell in cell_list:
      cell.value = indices[idn]
    worksh.update_cells(cell_list)
    idn=idn+1
  

  num=num+60

#Code to calculate recall and precision:

pn=56
num=902
for i in range(0,len(brid)):
  recall=0
  reca=0
  prec=0
  precision=0
  cids=[]
  t=True
  worksh = gc.open('Output-TF-IDF').sheet1
  out=worksh.get_all_values()
  print("---")
  while t==True:
    cids.append(rowsss[pn][2])
    if pn<200:
      pn=pn+1
    if rowsss[pn][1]!="":
      t=False
  for q in range(len(cids)):
    print(cids[q])
  
  cell_list = worksh.range('C'+str(num)+':C'+str(num+57))
  for cell in cell_list:
    cell.value = "No"
  worksh.update_cells(cell_list)

  for q in range(len(cids)):
    for p in range(num-1,num+57):
      if rows[int(cids[q])-1][0]==out[p][0]:
        cell_list = worksh.range('C'+str(p+1)+':C'+str(p+1))
        for cell in cell_list:
          cell.value = "Yes"
        worksh.update_cells(cell_list)
        
#Code to calculate average recall and average precision:

  worksh = gc.open('Output-TF-IDF').sheet1
  out=worksh.get_all_values()
  for p in range(num-1,num+57):
    prec=prec+1
    if out[p][2]=="Yes":
      reca=reca+1
      recall=reca/len(cids)
      precision=reca/prec
      cell_list = worksh.range('D'+str(p+1)+':D'+str(p+1))
      for cell in cell_list:
        cell.value = recall
      worksh.update_cells(cell_list)
      cell_list = worksh.range('E'+str(p+1)+':E'+str(p+1))
      for cell in cell_list:
        cell.value = precision
      worksh.update_cells(cell_list)     
    cell_list = worksh.range('D'+str(p+1)+':D'+str(p+1))
    for cell in cell_list:
      cell.value = recall
    worksh.update_cells(cell_list)
    precision=reca/prec
    cell_list = worksh.range('E'+str(p+1)+':E'+str(p+1))
    for cell in cell_list:
      cell.value = precision
    worksh.update_cells(cell_list) 
        

  num=num+60

#Code to calculate average recall and average precision:
  worksh = gc.open('Output-TF-IDF').sheet1
out=worksh.get_all_values()
num=1
j=2
k=1
for i in range(3541,3599):  
  rsum=0
  psum=0
  tsum=0
  for num in range(k,i,60):
    rsum=rsum+float(out[num][3])
    psum=psum+float(out[num][4])
    tsum=tsum+float(out[num][1])
  cell_list = worksh.range('H'+str(j)+':H'+str(j))
  for cell in cell_list:
    cell.value = j-1
  worksh.update_cells(cell_list)
  cell_list = worksh.range('I'+str(j)+':I'+str(j))
  for cell in cell_list:
    cell.value = rsum/60
  worksh.update_cells(cell_list)
  cell_list = worksh.range('J'+str(j)+':J'+str(j))
  for cell in cell_list:
    cell.value = psum/60
  worksh.update_cells(cell_list)
  cell_list = worksh.range('K'+str(j)+':K'+str(j))
  tsum=tsum+float(out[num][1])
  for cell in cell_list:
    cell.value = tsum/60
  worksh.update_cells(cell_list) 
  j=j+1
  k=k+1
