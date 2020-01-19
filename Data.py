#Author: Nico Loreto, University of Ottawa
#Author: Grant Wagner, University of Ottawa
#Team 2184, Jan. 19, 2020

import numpy
import requests
import pandas as pd
import re
import time
import urllib.request
import json
from bs4 import BeautifulSoup

def Alberta():

    Data = []
    
    url = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet'

    urllib.request.urlretrieve(url, 'AB.html')

    f = open('AB.html')

    soup = BeautifulSoup(f, features='lxml')

    last_update = str(soup.find(string = re.compile("Last Update")))
    last_update = last_update.replace(",",'')

    summary = soup.find("b",string=re.compile('SUMMARY')).find_parent("table")
    Data.append(["ALBERTA",last_update])

    def Table(table):
        table_content=[]
        ROWS = table.find_all("tr")
        for row in ROWS:
            row_content=[]
            COLUMNS = row.find_all("td")
            for column in COLUMNS:
                row_content.append(column.get_text())
            table_content.append(row_content)
        table_content.remove([])
        return table_content

    ABU = last_update
    Data = numpy.concatenate((Data,  Table(summary)), axis=0)
    return Data

def Ontario():
    
    url = 'http://reports.ieso.ca/public/RealtimeConstTotals/PUB_RealtimeConstTotals.xml'

    urllib.request.urlretrieve(url, 'ON.xml')

    f = open('ON.xml')

    soup = BeautifulSoup(f, features='lxml')

    last_update = str(soup.find("createdat"))
    last_update = last_update.replace("<createdat>",'')
    last_update = last_update.replace("</createdat>",'')
    last_update = last_update.replace("T",' ')
    Data = []
    Data.append(['',''])
    Data.append(["ONTARIO",'Updated: '+last_update])

    rows = soup.find_all('marketquantity')
    ONR=[]
    for row in rows:
        ONR.append(re.sub(re.compile('<(.*?)>'),"",str(row)))
        
    columns = soup.find_all('energymw')
    ONC=[]
    for col in columns:
        ONC.append(re.sub(re.compile('<(.*?)>'),"",str(col)))

    for i in range (0,7):
        Data.append([ONR[i],ONC[i]])

    return Data

def NewBrunswick():
    
    url = 'https://tso.nbpower.com/Public/en/SystemInformation_realtime.asp'

    urllib.request.urlretrieve(url, 'NB.html')

    f = open('NB.html')

    soup = BeautifulSoup(f, features='lxml')

    last_update = str(soup.find("i"))
    last_update = last_update.replace(',','')
    last_update = last_update.replace('Times at which values are sampled may vary by as much as 5 minutes.</i>','')
    last_update = last_update.replace('<i>','')
    
    Data = []
    Data.append(["",""])
    Data.append(["NEW BRUNSWICK","Updated: "+last_update])

    RData=[]
    CData=[]
    rows = soup.find_all(valign="top",string=re.compile("[A-Z]"))
    for row in rows:
        row = re.sub(re.compile('<(.*?)>'),"",str(row))
        RData.append(row.replace('\xa0',''))
    RData = RData[2:]

    cols = soup.find(id="nb-load").find_parent("tr")
    for col in cols:
        col = re.sub(re.compile('<(.*?)>'),"",str(col))
        CData.append(col.rstrip())
    CData[:] = (value for value in CData if value != '')

    for i in range (0,10):
        Data.append([RData[i],CData[i]])
    return Data

def NovaScotia():

    Data=[]

    url = 'https://www.nspower.ca/clean-energy/todays-energy-stats#%20'

    urllib.request.urlretrieve(url, 'NS.html')

    f = open('NS.html')

    soup = BeautifulSoup(f, features='lxml')

    last_update = str(soup.find(class_="ppcl-date"))
    last_update = last_update.replace(',','')
    last_update = re.sub(re.compile('<(.*?)>'),"",str(last_update))

    Data.append(['',''])
    Data.append(['NOVA SCOTIA',"Updated: "+last_update])

    avail_cap = soup.find_all('strong')
    avail_cap = avail_cap[1]
    avail_cap = re.sub(re.compile('<(.*?)>'),"",str(avail_cap))
    avail_cap = avail_cap.replace(",",'')
    Data.append([avail_cap.split(" ")[1]+" "+avail_cap.split(" ")[2],avail_cap.split(" ")[0]])

    req = requests.get("https://www.nspower.ca/library/CurrentLoad/CurrentLoad.json")
    req = list(req.json())
    req = str(req[len(req)-1])
    req = re.findall(r'\b\d+\b', req)
    req = req[1]
    
    Data.append(['Current Load',req])
    return Data
 
    
ABData = Alberta()
ONData = Ontario()
NBData = NewBrunswick()
NSData = NovaScotia()

Data = numpy.concatenate((ABData, ONData, NBData, NSData ), axis=0)

NPData = numpy.asarray(Data)
numpy.savetxt('Data.csv',NPData,delimiter=',',fmt='%s',header="SUMARY,ENERGY(MW)",comments="")












