import requests
from bs4 import BeautifulSoup
import csv
import time
import html
import datetime


#######################GLOBAL VARIABLES################################################

#Daily_Web_URL_part_1 = "https://spotcrime.com/ca/san+jose/daily-blotter/"
Daily_Web_URL_part_1 = "https://spotcrime.com/ut/salt+lake+city/daily-blotter/"
Start_Year = 2018
Start_Month = 5
Start_Day = 19
csv_file = "Class_test_eddie.csv"
sleep_timer = 2
#When stop date is None it will use the date the script was started on.
stop_date = None
#stop_date = "31/12/2009"  # Takes it as Day/Month/Year


def time_convertion(time):
    check = True
    try:
        hour = int(time[1][:-3])
        min = int(time[1][3:])
        #print("----------------------")
        #print(hour, min)
        #print("______________________")
        if hour == 12:
            hour = 0
        if time[2] == 'PM':
            hour = hour + 12
        timestamp = ("%s %s:%s" % (time[0], str(hour).zfill(2), str(min).zfill(2)))
        time_flag = 0
    except Exception:
        print("Standard TimeStamp Not Detected")
        time_flag = 1
        check = False
    if check == False:
        print("ONLY ADDING: ", time[0])
        timestamp = time[0]
    return timestamp, time_flag




#Method to request data from site, and return its contents to the variable for the find command.

def request_page(site):
    loop = True
    soup = ""
    while loop == True:
        try:
            # This code goes ahead and grabs the html code from nay website given.
            page = requests.get(site)

            contents = page.content

            #bs4 organization
            soup = BeautifulSoup(contents, 'html.parser')
            # Assigned all tags of td to a variable that is a list of all such tags.
            #td_tag = soup.find_all('tr')
        except Exception:
            print(site, ": FAILED")
            print("Trying again in five seconds")
            time.sleep(5)
        #Stops loop from continuing when successful.
        if soup != "":
            loop = False

    return soup
################################################################################
#Method to create list of dates to feed to the url string.
#zfill(number) only works on a string
def dates():
    if stop_date == None:
        timestamp = datetime.datetime.today()
        stopdate = timestamp.strftime("%d/%m/%Y")
    else:
        stopdate = stop_date
    #print(stopdate)
    d = Start_Day
    m = Start_Month
    y = Start_Year
    Dates_List = []
    date_loop = True
# for loop that generates dates.
    while date_loop == True:

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
        date = (str(d).zfill(2) + "/" + str(m).zfill(2) + "/" + str(y))

        #print(date)
        #printing as a tuple to get the output correct.
        Dates_List.append("%s-%s-%s" %  (year, month, day))

        d += 1
        if date == stopdate:
            date_loop = False
    return Dates_List
################################################################################
# Dynamic Web URL
Dates = dates()

#First part of webname
Web_Page = Daily_Web_URL_part_1

#counter = 0
#w = open("unicode_test.txt", "w")

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Crime', 'Date', "Address", "Lat", 'Long', 'Details', 'Casenumber', 'Link', 'No_Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for D in Dates:
        URL = Web_Page + D
        print("--" * 20)
        print(URL)
        # Test Page: "https://spotcrime.com/ca/san+jose/daily-blotter/2018-03-26"
        soup = request_page(URL)
        #Sleep time for days page
        time.sleep(sleep_timer)

        #for loop to grab information from the table before getting lat and long from the details link
        #if date does not exist this loop does not execute thus skipping the date.
        for tr in soup.find_all('tr')[1:]: # the number determines where in the table to start collecting data.
            link = str(tr.find_all('a',href=True))
            tds = tr.find_all('td')
            Crime = tds[1].text
            Datee = tds[2].text
            Address = tds[3].text
            print(Crime, Datee, Address)
            ###############################
            #Code to format timestamp into suitable format for postgresql
            Datee = Datee.replace("/", "-")
            Datee = Datee.replace(".", "")
            #######DATEE INTO A LIST TO CONVERT INTO MILITARY TIME#########
            time_list = Datee.split(" ")
            ##########GIVES Datee the formated version for PostGreSQL#############
            Datee = time_convertion(time_list)
            print(Datee[0])


##########################################################################
            # Using a continue to pass over "Other" crime categories
            #if Crime == "Other":
            #    print("Other Detected: Skipping")
            #    continue

###########################################################################
# Sleeps for a second to avoid server lockout
            time.sleep(sleep_timer)
############################################################################
            #Next This section gets the link from the table and requests it
            link = link[10:-30]
            link = ('%s%s' % ('https://spotcrime.com', link))
            #### ADD TRY CATCH TO ATTEMPT TO SPEED UP WEBSCRAPPING############
            coor_soup = request_page(str(link))

#############################################################################
            # This section gets the lat and long of that specific page.(Commented out code was first attempt (worked but final
            # version is more reliable))
            #Gets string of meta that has the lat long
            coor_lat = str(coor_soup.find("meta", itemprop="latitude"))
            #coor_long = str(coor_soup.find("meta", itemprop="longitude"))
            ######## Gets Details from second page ##########
            details = str(coor_soup.find("blockquote"))
            details = details[16:-18]
            details = html.unescape(details) # removes HTML syntax from special characters.
            print(details)
            ############## Gets CASE NUMBER #########################
            casenum = ""
            try:
                casenum = str(coor_soup.find_all("dd")[4]) # Gets all dd as a list and gets the fifth element
                casenum = casenum[4:-5].strip()
                print( "CODE:", casenum)
            except Exception:
                print("NO CASENUMBER DETECTED")

            coor_space = coor_lat.replace('"', ' ')
            #print("------------------------")

            try:
                #Splits string so that the lat and long will be in list at element 2 and 8
                coor_list = coor_space.split()

                #print("------------------------")
                #print(coor_lat)
                lat = coor_list[2]
                long = coor_list[8]
                #print(coor_list[2], coor_list[8])
                #print("------------------------")
            except Exception:
                print("------FAILED--------" * 20)
                print("------FAILED--------" * 20)
                print("------FAILED--------" * 20)
                print(coor_list)
                print(coor_space)
                print(coor_lat)
                print("------FAILED--------" * 20)
                print("------FAILED--------" * 20)
                print("------FAILED--------" * 20)
                #Changes lat to empty string so data can keep being collected.
                lat = "0"
                long = "0"
            print(link, lat, long)

##############################################################################
            #Copys all scraped information into the csv.
            writer.writerow({'Crime': str(Crime), 'Date': str(Datee[0]), 'Address': str(Address), 'Lat': str(lat), 'Long': str(long), 'Details': str(details),'Casenumber':casenum, 'Link':str(link), 'No_Time': str(Datee[1])})

print("----------------------DONE------------------------")