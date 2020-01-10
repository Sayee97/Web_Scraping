# Web_Scraping
MINDS USC Research

URL: https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches

# Languages Used: Python3
Parsing tool: Beautiful Soup (Python Package for parsing HTML files)

Logic: 
1. Extract rowspan of first line to get number of launchpads. Further, check if its successful, en route or operational and increment the count.
2. Convert the dates to ISO 8601 format
3. Add all dates in the year 2019 and give a default value 0 if no launchpad was present on that day
4. Convert the result into desired CSV file as output

