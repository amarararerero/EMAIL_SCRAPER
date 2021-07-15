import bs4
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import os

os.system('clear')
os.system('figlet -w 1000 -f poison EMAIL SCRAPER | lolcat')

Target_Url = str(input("[+] Enter Target Url to Scan : "))
Urls = deque([Target_Url])

Scraped_Urls = set()
Email = set()

count = 0
try:
    while len(Urls):
        count += 1

        if count == 100:
            break

        Url = Urls.popleft()
        Scraped_Urls.add(Url)
        Parts = urllib.parse.urlsplit(Url)
        Base_Url = '{0.scheme}://{0.netloc}'.format(Parts)
        Path = Url[:Url.rfind('/')+1] if '/' in Parts.path else Url
        print('[%d] Lets Scraped %s' %(count , Url))

        try:
            Response = requests.get(Url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", Response.text, re.I))
        Email.update(new_emails)

        Soup = bs4.BeautifulSoup(Response.text, features="lxml")

        for anchor in Soup.find_all("a"):
            Link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if Link.startswith('/'):
                Link = Base_Url + Link
            elif not Link.startswith('http'):
                link = Path + Link
            if not Link in Urls and not Link in Scraped_Urls:
                Urls.append(Link)

except KeyboardInterrupt:
    print('\n[-] Closinggggggggg\n')

for mail in Email:
    print("[i] ",mail)
