#!/usr/bin/env python

"""
The tiniest Nagios dashboard. Scrapes status.cgi, returns
ANSI-colored host & service counts.

Not guaranteed to work at all. For best chance of results,
use url akin to https://myhost/nagios3/cgi-bin/status.cgi

Sam Merwin, March 2014
smerwin@gmail.com
"""

import requests
from random import randrange
from bs4 import BeautifulSoup as bs
# colors provided by ansicolors package
from colors import red, yellow, green, bold
from argparse import ArgumentParser as argparse
#from time import strftimedd

# We use Nagios return codes
# 0 = OK
# 1 = Warn
# 2 = Critical
# 3 = Unknown
retval = 0

# get yo args
parser = argparse(description="Nagios status.cgi scraper, return tiny overview")
parser.add_argument("-H", "--host", help="URL to nagios3/cgi-bin/status.cgi",
                                    required=True)
parser.add_argument("-u", "--user", help="HTTP Basic Auth user")
parser.add_argument("-p", "--password", help="HTTP Basic Auth pass")
args = parser.parse_args()

# override user/pass here if you wish
# args.user = ""
# args.password = ""

def print_table(table):
    # Print colorized counts for each status
    # Do not print if count is 0
    headers = list()
    cells = list()
    global retval
    ths = table.find_all('th')
    tds = table.find_all('td')
    for th in ths:
        headers.append(th.getText())
    for td in tds:
        cells.append(td.getText())
    results = dict(zip(headers,cells))

    for key, val in results.items():
        if key in ("Up Ok") and val != "0":
            print "{0}: {1}".format(key, green(val))
        elif key in ("Down Critical") and val != "0":
            print "{0}: {1}".format(red(key), red(val))
            retval = 2
        elif key in ("Warning") and val != "0":
            print "{0}: {1}".format(key, yellow(val))
            retval = 1
        elif key in "Pending" and val != "0":
            print "{0}: {1}".format(key, val)
        elif key in ("Unreachable Unknown") and val != "0":
            print "{0}: {1}".format(key, val)
            retval = 3
        else:
            continue

def print_title(string):
    # Colorize title based on retval
    if retval == 0:
        string = green(string)
    elif retval == 2:
        string = red(string)
    else:
        string == yellow(string)
    print bold(string)

# Get nagios page
r = requests.get(args.host, auth=(args.user,args.password), verify=False)
# 200 or bust
r.raise_for_status()
# Parse it into soup
soup = bs(r.text)

# Find the host and service totals tables
hostTotals = soup.find('table',{'class':'hostTotals'})
serviceTotals = soup.find('table',{'class':'serviceTotals'})

# randomly futzing with the title to prove we haven't stalled
title = list("NAGIOS")
i = 0
while i < (randrange(0,3)):
    rand_index = randrange(0,len(title))
    title[rand_index] = title[rand_index].lower();
    i+= 1
title = ''.join(title)

# Print results.
print_title(title)
print bold("hosts")
print_table(hostTotals)
print bold("services")
print_table(serviceTotals)
# optionally, print time
# print "\n\n{0}".format(strftime("%H:%M:%S"))

exit(retval)
