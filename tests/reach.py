#import urllib

#res=urllib.request.urlopen("https://www.facebook.com/wagnerpyter/friends")
#
#import requests
#from bs4 import BeautifulSoup
#
##url = "http://uswest.ensembl.org/Gallus_gallus/Gene/Summary?db=core;g=ENSGALG00000016955;r=1:165302186-165480795;t=ENSGALT00000027404"
#url="https://www.facebook.com/wagnerpyter/friends"
#r = requests.get(url, timeout=5)
#html = BeautifulSoup(r.text)
##description = html.find("div", {'class': "rhs"})
#description = html.find("div", {'class': "fsl fwb fcb"})
#print(description.text)
#
#import requests
#
#r = requests.get("https://www.facebook.com/wagnerpyter/friends")
#import webbrowser
#
#b=webbrowser.get("firefox")
#c=b.open("https://www.facebook.com/wagnerpyter/friends")

from splinter import Browser
browser=Browser()
url = "http://www.google.com"
url="https://www.facebook.com/wagnerpyter/friends"
#url="https://www.facebook.com/adalberto.ferroz"
browser.visit(url)
#browser.fill('q', 'splinter - python acceptance testing for web applications')
#browser.fill("email","greenkobold@gmail.com")
#browser.fill("pass","Jockey67")
#browser.find_by_value("Log In").click()

#url="https://www.facebook.com/wagnerpyter/friends"
#url="https://www.facebook.com/adalberto.ferroz"
browser.visit(url)
#button = browser.find_by_name('btnG')
## Interact with elements
#button.click()

#if browser.is_text_present('splinter.readthedocs.org'):
if browser.is_text_present('antenna'):
    print("Yes, the official website was found!")
else:
    print("No, it wasn't found... We need to improve our SEO techniques")
