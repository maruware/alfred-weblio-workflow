#!/usr/bin/python
# encoding: utf-8

import sys
import re

from workflow import Workflow

import urllib2
import urllib
from bs4 import BeautifulSoup

def parse(url):
    res = urllib2.urlopen(url)
    html = res.read()

    soup = BeautifulSoup(html, "html.parser")
    explanation_elems = soup.select('#summary div.summaryM.descriptionWrp .content-explanation')

    if len(explanation_elems) == 0:
        return []
    
    text = explanation_elems[0].text
    if text.find(u'、') > -1:
        return text.split(u'、')
    if text.find(u'; ') > -1:
        return text.split(u'; ')

    return []

def search(query):
    q = urllib.quote(query.encode('utf-8'))
    url = u'http://ejje.weblio.jp/content/' + q
    items = parse(url)

    return items

def main(wf):
    args = wf.args
    query = args[0]
    items = search(query)

    for item in items:
        wf.add_item(item, arg=item, valid=True)        
    wf.send_feedback()

if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    sys.exit(wf.run(main))