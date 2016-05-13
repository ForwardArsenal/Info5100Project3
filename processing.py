#import urllib2
import json
from bs4 import BeautifulSoup
import csv
import requests
import itertools
from multiprocessing import Pool, Manager
#output = open("/Users/WeiXing/Desktop/movies_budget.txt", "w")

#url = "http://www.the-numbers.com/movie/budgets/all"

#page = urllib2.urlopen(url)
data = list()
titles = list()
newData = list()
manager = Manager()
movieMap = manager.dict()

def generateCSVData(year):
    for row in table.findAll("tr")[1:]:
        tmpArr = []
        cells = row.findAll("td")
        if(not cells):
            continue
        
        release_date = cells[1].findAll(text=True)[0].encode("utf-8")
       
        if(int(release_date.split("/")[2]) != year):
            continue

        title = cells[2].findAll(text=True)[0].encode("utf-8")
        budget = cells[3].findAll(text=True)[0].encode("utf-8")
        domestic_gross = cells[4].findAll(text=True)[0].encode("utf-8")
        worldwide_gross = cells[5].findAll(text=True)[0].encode("utf-8")

        tmpArr.append(title)
        tmpArr.append(release_date)
        tmpArr.append(budget)
        tmpArr.append(domestic_gross)
        tmpArr.append(worldwide_gross)
        
        titles.append(title)

        data.append(tmpArr)


def apiCall(title):
    #call api to get supplementary information about the movie
    tmpArr = []
    extra_fields = ["Genre", "Director", "Awards", "imdbRating"]
    url = "http://www.omdbapi.com/?t="+title+"&y=&plot=short&r=json"
    response = requests.get(url).text
    respDict = json.loads(response)
    if("Error" in respDict):
        print(respDict["Error"])
        for field in extra_fields:
            tmpArr.append("None")
        print("Success!")
    else:
        for field in extra_fields:
            tmpArr.append(respDict[field].encode("utf-8"))
    movieMap[title] = tmpArr

def writeToCSV(year):
    for record in data:
        title = record[0]
        extraInfo = movieMap[title]
        newData.append(record+extraInfo)

    with open("/Users/WeiXing/Desktop/movie_budgets/movie_budget_"+str(year)+".csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvHeader = ["Title", "Release Date", "Budget", "Domestic Gross", "Worldwide Gross", "Genre", "Director", "Awards", "imdbRating"]
        csvwriter.writerow(csvHeader)
        csvwriter.writerows(newData)


if __name__ == '__main__':
    input = open("/Users/WeiXing/Desktop/movie_budgets.html", "r")
    soup = BeautifulSoup(input)

    table = soup.find("table", { "id": "budgets" })
    generateCSVData(2015)
    print("The length of titles list is "+str(len(titles)))
    p = Pool(len(titles))
    p.map(apiCall, titles)
    
    writeToCSV(2015)



          








    

   