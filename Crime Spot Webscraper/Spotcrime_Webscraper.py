import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import urllib.request
#import regex

#Method to request data from site, and return its contents to the variable for the find command.

def request_page(site):

    # This code goes ahead and grabs the html code from nay website given.
    page = requests.get(site)

    contents = page.content

    #bs4 organization
    soup = BeautifulSoup(contents, 'html.parser')
    # Assigned all tags of td to a variable that is a list of all such tags.
    #td_tag = soup.find_all('tr')

    return soup
################################################################################
#Method to create list of dates to feed to the url string.
#zfill(number) only works on a string
def dates():
    d = 1
    m = 1
    y = 2017
    Dates_List = []
# for loop that generates dates.
    for n in range(3080):

        if d > 31:
            d = 1
            m += 1
        if m > 12:
            y += 1
            m = 1
            d = 1
# Code that prints out code in string format <BOOKMARKS>
        #Day variables
        day = str(d).zfill(2)
        month = str(m).zfill(2)
        year = str(y)
        date = (str(d).zfill(2),"/",str(m).zfill(2),"/",str(y))
        date_str = str(date)
        date_final = date_str.replace(" ", "")
        #print(date)
        #printing as a tuple to get the output correct.
        Dates_List.append("%s-%s-%s" %  (year, month, day))

        d += 1
    return Dates_List
################################################################################
# Dynamic Web URL
Dates = dates()

# "https://spotcrime.com/ca/san+jose/daily-blotter/2018-03-22"  <-Backup

#First part of webname
Web_Page = "https://spotcrime.com/ca/san+jose/daily-blotter/"

#Opens up csv to write too
'''
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
'''

#counter = 0
#w = open("unicode_test.txt", "w")

with open('Spotcrime.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Crime', 'Date', "Address", "Lat", 'Long', 'Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for D in Dates:
        URL = Web_Page + D
        print(URL)
        # Test Page: "https://spotcrime.com/ca/san+jose/daily-blotter/2018-03-26"
        soup = request_page(URL)

        time.sleep(2)
# Code for testing, limits how many pages are webscraped
        '''
        counter += 1
        if counter == 2:
            #w.close()
            break
        '''
        #for loop to grab information from the table before getting lat and long from the details link
        for tr in soup.find_all('tr')[2:]:
            link = str(tr.find_all('a',href=True))
            tds = tr.find_all('td')
            Crime = tds[1].text
            Datee = tds[2].text
            Address = tds[3].text
            print(Crime, Datee, Address)
##########################################################################
            # Using a continue to pass over "Other" crime categories
            if Crime == "Other":
                print("Other Detected: Skipping")
                continue

###########################################################################
# Sleeps for a second to avoid server lockout
            time.sleep(2)
############################################################################
            #Next This section gets the link from the table and requests it
            link = link[10:-30]
            link = ('%s%s' % ('https://spotcrime.com', link))
            coor = requests.get(str(link))
            coor_page = coor.content

#############################################################################
            # This section gets the lat and long of that specific page.(Commented out code was first attempt (worked but final
            # version is more reliable))
            coor_soup = BeautifulSoup(coor_page, 'html.parser')
            #Gets string of meta that has the lat long
            coor_lat = str(coor_soup.find("meta", itemprop="latitude"))
            #coor_long = str(coor_soup.find("meta", itemprop="longitude"))

            #lat = coor_lat[15:-82]
            #long = coor_long[15:-24]

            coor_space = coor_lat.replace('"', ' ')
            #print("------------------------")

            #Splits string so that the lat and long will be in list at element 2 and 8
            coor_list = coor_space.split()


            # FOR LOOP TO QUICKLY CHECK that the string has been split.
            '''
            for word in coor_list:
                print(word)
            '''
            #print("------------------------")
            #print(coor_lat)
            lat = coor_list[2]
            long = coor_list[8]
            #print(coor_list[2], coor_list[8])
            #print("------------------------")
            print(link, lat, long)


        #page = requests.get(site)

        #contents = page.content

        # bs4 organization
        #soup = BeautifulSoup(contents, 'html.parser')

##############################################################################


            #Copys all scraped information into the csv.
            writer.writerow({'Crime': str(Crime), 'Date': str(Datee), 'Address': str(Address), 'Lat': str(lat), 'Long': str(long), 'Link':str(link)})


# Example Code for writing into a blank CSV

'''


    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

'''

print("----------------------DONE------------------------")

