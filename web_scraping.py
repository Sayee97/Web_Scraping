import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import dateutil.parser as parserTime
import numpy


##########Convert all Dates to ISO 8601 Format
def convertToISO(k):
	indexOfOpeningBraces = k.find('[')
	if indexOfOpeningBraces != None:
		k = k[:indexOfOpeningBraces]
	if '(ground test)' in k:
		index11 = k.find('(')
		k = k[:index11]
	k = "2019 "+ k
	k = parserTime.parse(k).date()
	k = k.isoformat()
	return k

######### Use Beautiful Soup and parse the given URL to find rows
def parse(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	table_html = soup.find('table', class_ = 'wikitable collapsible')
	data = []
	table_body = table_html.find('tbody')
	rows = table_body.find_all('tr')
	return rows

######### Logic to extract distinct number of launch pad on a particular date
def countLaunchPads(rows):
	rowNum = 0
	store_date_and_value = {}
	while(rowNum<len(rows)):
		table_cell = rows[rowNum].find_all('td')
		if table_cell and table_cell[0].get('rowspan') != None and  int(table_cell[0].get('rowspan'))>1:
			numberOfLanchPads = int(table_cell[0].get('rowspan'))
			temp = 1
			count = 0
			while(temp <= numberOfLanchPads):
				table_data = rows[rowNum].find_all('td')
				outcome = table_data[-1].text.strip()
				if outcome == "Operational" or outcome == "Successful" or outcome == "En route":
					count += 1
				rowNum += 1
				temp += 1
			keyFormatISO = convertToISO(table_cell[0].text)
			if keyFormatISO in store_date_and_value:
				store_date_and_value[keyFormatISO] += count
			else:

				store_date_and_value[keyFormatISO] = count
		else:
			rowNum += 1
	return store_date_and_value

######### Adding all the dates of 2019 and giving default value 0 if there are no launches
def add_all_dates(d):

	idx = pd.date_range('01-01-2019', '31-12-2019')
	s = pd.Series(d)
	s.index = pd.DatetimeIndex(s.index)
	s = s.reindex(idx, fill_value = 0)
	s = s.values.tolist()
	i = 0
	finald = {}
	for i in range(365):
		finald[idx[i].isoformat()] = s[i]
	return finald


######### Call all functions and convert into CSV file
def main():
	url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
	rows = parse(url)
	date_and_value = countLaunchPads(rows)
	allValues = add_all_dates(date_and_value)
	OrbitalLaunches = pd.DataFrame(list(allValues.items()), columns=['date', 'value'])
	#print(OrbitalLaunches)
	OrbitalLaunches.to_csv('OrbitalLaunches.csv')

if __name__ == "__main__":
    main()










