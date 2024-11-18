import requests
from bs4 import BeautifulSoup
import json

POINTR_PATENTS_LIST = [
    'US10324197', 
    'US11029415', 
    'US11169280',
    'US10378907',
    'US10883833',
    'US10511971',
    'US11240663',
    'US11297497',
    'US10834528',
    'US11356810',
    'US11356810',
    'US11514633',
    'US10511971',
    'US11240663',
    'US11297497',
    'US11716616'
]

GOOGLE_PATENTS_URL_PRE = 'https://patents.google.com/patent/'
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}


def get_desc_keyword_freq(soup):
    desc_text = soup.find('section',{'itemprop':'description'}).get_text()

    symbol_list = [',', '.', "'", '"', ")", "(", "-"]

    for s in symbol_list:
        desc_text = desc_text.replace(s, "")

    from collections import defaultdict
    temp = dict()


    for wrd in desc_text.split():
            try:
                temp[wrd] += 1
            except:
                temp[wrd] = 1  
    
    # getting max frequency
    res = max(temp, key=temp.get)
    
    items = list(temp.items())

    # Sort the list of tuples by the value (second element)
    items.sort(key=lambda x: x[1])

    # Convert the sorted list of tuples back to a dictionary
    sorted_data = dict(items)

    # Convert the dictionary to JSON
    sorted_json = json.dumps(sorted_data, indent=4)

    return sorted_json

def get_id(soup):
     id = soup.find('span',itemprop='publicationNumber').get_text()
     return id

def get_title(soup):
     title = soup.find('meta',attrs={'name':'DC.title'})['content'].rstrip()
     return title

def get_assignee(soup):
    return soup.find('dd',itemprop='assigneeCurrent').text.strip()

def get_pubdate(soup):
     pubdate = soup.find('td',itemprop='priorityDate').get_text()
     return pubdate

def get_forward_citations(soup):
    citations = soup.find_all('tr',{'itemprop':'forwardReferencesOrig'})
    l = []
    for tr in citations:
        a = tr.find_all('span')[0].contents[0]
        l.append(a)
    return l

def get_forward_family_citations(soup):
    citations = soup.find_all('tr',{'itemprop':'forwardReferencesFamily'})
    l = []
    for tr in citations:
        a = tr.find_all('span')[0].contents[0]
        l.append(a)
    return l

def get_backward_citations(soup):
    citations = soup.find_all('tr',{'itemprop':'backwardReferences'})
    l = []
    for tr in citations:
        a = tr.find_all('span')[0].contents[0]
        l.append(a)
    return l

def get_backward_family_citations(soup):
    citations = soup.find_all('tr',{'itemprop':'backwardReferencesFamily'})
    l = []
    for tr in citations:
        a = tr.find_all('span')[0].contents[0]
        l.append(a)
    return l

def request_page(patent_id):
    page_html = requests.get(
                    f'{GOOGLE_PATENTS_URL_PRE}{patent_id}/en', 
                    headers = HEADERS
    ).content

    soup = BeautifulSoup(page_html, 'html.parser')
    
    return soup

def json_builder(patent_id):
    soup = request_page(patent_id)
    title = get_title(soup)
    assignee = get_assignee(soup)
    pubdate = get_pubdate(soup)
    fw_citations = get_forward_citations(soup)
    fw_fm_citations = get_forward_family_citations(soup)
    bw_citations = get_backward_citations(soup)
    bw_fm_citations = get_backward_family_citations(soup)

    json = {
        'id': patent_id,
        'title': title,
        'assignee': assignee,
        'pubdate': pubdate,
        'forward_citations': fw_citations,
        'forward_family_citations': fw_fm_citations,
        'backward_citations': bw_citations,
        'backward_family_citations': bw_fm_citations
    }

    return json


if __name__=="__main__":
    out = json_builder('US11356810')
    print(out)
