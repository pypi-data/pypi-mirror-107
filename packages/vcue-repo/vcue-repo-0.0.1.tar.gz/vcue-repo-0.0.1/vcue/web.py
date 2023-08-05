from bs4 import BeautifulSoup
import string
import urllib
from urllib.parse import quote

def fresh_soup(url):    
    '''
    Collects and parses the page source from a given url, returns the parsed page source 
    - url : the url you wish to scrape
    '''
    hdr = {'User-Agent': 'Mozilla/5.0'}                                       # we will browse as if using the Mozilla Browser
    
    try: 
        req = urllib.Request(url,headers=hdr)                                 # make a url request using the specified browser
        source = urllib.urlopen(req,timeout=10).read()                        # retrieve the page source
        
    except:                                                                   # if the url is reject due to non formatted characters 
        url = clean_url(url)
        
        req = urllib.Request(url,headers=hdr)                                 # the url should be readable now 
        source = urllib.urlopen(req,timeout=10).read()                        
            
    soup = BeautifulSoup(source,"lxml")                                       # process it using beautiful soup 
    
    return soup

def clean_url(url):
    '''Clean urls with non-english characters such as tildes'''
    non_conformists = [s for s in url if s not in string.printable]       # we get a list of the troublemaker characters 
    for s in non_conformists:
        url = url.replace(s,quote(s))       # and use the quote function from urllib.parse to translate them 
    return url