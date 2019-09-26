import re
import requests
from bs4 import BeautifulSoup 
import sys
import os

baseUrl = "http://factordb.com/"
def n_to_primes(n):
    myVars = []
    r = requests.get(baseUrl+"index.php?query="+n)
    html = r.content
    mylist =[]
    soup = BeautifulSoup(html,"lxml")
    tables = soup.findAll("table")
    for table in tables:
         if table.findParent("table") is None:
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                mylist.append(str(cells))
    data = mylist[3]
    data = data.split(",")
    soup2 = BeautifulSoup(data[0],"lxml")
    for row in soup2.findAll("td"):
        status = row.text # Get the status

    links = []
    soupLinks = BeautifulSoup(data[2],"lxml")
    for row in soupLinks.findAll("a"):
        links.append(row["href"])
    l = len(links)
    myVars.append([status,links[l-2],links[l-1]])
    return myVars


def get_prime(p):
    r = requests.get(baseUrl+p)
    html = r.content
    soup = BeautifulSoup(html,"lxml")
    try:
        value = soup.find('input', {'name': 'query'}).get('value')
        return value
    except:
        print "Fail"
