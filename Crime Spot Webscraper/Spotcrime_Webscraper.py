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
    d = 8
    m = 7
    y = 2012
    Dates_List = []
# for loop that generates dates.
    for n in range(2160):

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
    fieldnames = ['Crime', 'Date', "Address"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for D in Dates:
        URL = Web_Page + D
        print(URL)
        soup = request_page(URL)

        time.sleep(1)

        #counter += 1
        #if counter == 5:
            #w.close()
            #break

        for tr in soup.find_all('tr')[2:]:
            tds = tr.find_all('td')
            Crime = tds[1].text
            Datee = tds[2].text
            Address = tds[4].text
            print(Crime, Datee, Address)
            #w.write(Crime + Datee + Address)
            writer.writerow({'Crime': str(Crime), 'Date': str(Datee), 'Address': str(Address)})


# Example Code for writing into a blank CSV

'''


    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

'''
'''
def request_page(site):

    # This code goes ahead and grabs the html code from nay website given.
    page = requests.get(site)

    contents = page.content

    #bs4 organization
    soup = BeautifulSoup(contents, 'html.parser')
    # Assigned all tags of td to a variable that is a list of all such tags.
    return soup


def date_range():
    day = 0
    year = 0
    month = 0


page = "https://spotcrime.com/ca/san+jose/daily-blotter/2018-03-22"

Data = request_page(page)

for tr in Data.find('tr')[2:]:
    tds = tr.find_all('td')
    print("Crime: ", tds[1].text)


'''

#counter = 40

#for tr in soup.find_all('tr')[2:]:
#    tds = tr.find_all('td')
#    print "Crime: %s, Date: %s, Address: %s, Link: %s" % \
#          (tds[1].text, tds[2].text, tds[3].text, tds[4].text)

#for n in xrange(counter):
    #print type(n)
#    reg = regex.compile(r"\b[0-9]{1,3}(?:\s\p{L}+)+")
    #reg = regex.compile(r"\d{1,5}\s\w.\s(\b\w*\b\s){1,2}\w*\.")
#    reg_M = regex.match("Theft", str(td_tag[n]))
#    print reg_M

 #   text = str(td_tag[n])
 #   print text

    #print td_tag[n]
    #print reg.search(str(td_tag[n]))
    #print"___________________________________________"
    #print reg_M.match(str(td_tag[n]))

print("----------------------Test Output Bellow------------------------")

