
import requests
from bs4 import BeautifulSoup
import csv
import re
import time
#import regex

w = open("unicode_test.txt", "w")

w.write("Hello")

w.close()

with open('Spotcrime.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Crime', 'Date', "Address"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    Dates = ["Bitch", "Please", "No", "you", "Pickles", "Wabalubadubdab"]

    for D in Dates:

        writer.writerow({'Crime': D, 'Date': D, 'Address': D})

