#import urllib2
import json
from bs4 import BeautifulSoup
import csv
import requests
import itertools
#output = open("/Users/WeiXing/Desktop/movies_budget.txt", "w")

#url = "http://www.the-numbers.com/movie/budgets/all"

#page = urllib2.urlopen(url)
input = open("/Users/WeiXing/Desktop/movie_budgets.html", "r")
soup = BeautifulSoup(input)

table = soup.find("table", { "id": "budgets" })
data = []
#print(table)
#print(soup.prettify())
for row in table.findAll("tr")[1:]:
	tmpArr = []
	cells = row.findAll("td")
	if(not cells):
		continue
	
	tmpArr.append(cells[2].findAll(text=True)[0].encode("utf-8"))
	tmpArr.append(cells[1].findAll(text=True)[0].encode("utf-8"))
	tmpArr.append(cells[3].findAll(text=True)[0].encode("utf-8"))
	tmpArr.append(cells[4].findAll(text=True)[0].encode("utf-8"))
	tmpArr.append(cells[5].findAll(text=True)[0].encode("utf-8"))

	data.append(tmpArr)
# generate the csv file from the html table of the movie budget website
with open("/Users/WeiXing/Desktop/movie_budget.csv", "w") as csvfile:
	csvwriter = csv.writer(csvfile)
	csvHeader = ["Title", "Release Date", "Budget", "Domestic Gross", "Worldwide Gross"]
	#print(jsonData[0])
	csvwriter.writerow(csvHeader)
	csvwriter.writerows(data)

# generate the supplementary csv file containing extra information of a given movie
jsonArr = []
newcsvHeader = ["Title", "Genre", "Director", "Awards", "imdbRating"]
with open("/Users/WeiXing/Desktop/movie_budget.csv", "r") as csvfile:
	csvreader = csv.reader(csvfile)
	csvheader = next(csvreader)
	for i in range(100):
		row = csvreader.next()
		title = row[0].replace(" ", "+")
		#print(title)
		url = "http://www.omdbapi.com/?t="+title+"&y=&plot=short&r=json"
		#print(url)
		response = requests.get(url).text
		jsonArr.append(response)
newData = []
for item in jsonArr:
	tmpArr = []
	respDict = json.loads(item)
	if("Error" in respDict):
		print(respDict["Error"])
		continue
	else:
		for field in newcsvHeader:
			tmpArr.append(respDict[field].encode("utf-8"))
	newData.append(tmpArr)

	

#print(newData)
#generate new csv file
with open("/Users/WeiXing/Desktop/supplementary_data.csv", "w") as newcsvfile:
    csvwriter = csv.writer(newcsvfile)
    csvwriter.writerow(newcsvHeader)
    csvwriter.writerows(newData)
 


          








    

   