import requests, json
import xml.etree.ElementTree as ET 
cookies = {
    's_fid': '737292652352B94A-2D08793FBB1D9F7B',
    'WRUID': '856361669.2096977450',
    '__CT_Data': 'gpv=4&apv_16437_www03=4&cpv_16437_www03=4&rpv_16437_www03=4',
    'TSda6109': '89379f8a0635d2ed54b7e732487471b2a69d52426956d14955e0b2bf1620e67a53cfc05d12c5ee39ffffffff19a8faf4ffffffff54b74eb2ffffffff',
    'accessibility': 'false',
    '__utma': '8697514.953585774.1416716822.1441819359.1441819359.1',
    '__utmc': '8697514',
    '__utmz': '8697514.1441819359.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '_ga': 'GA1.2.953585774.1416716822',
    'IDMSESSID': '100605285',
    'TSdde4ce': '52b87284d0b13cc81669010bf1169713f4bbbdaeaa37736b55e0aaa1bc093005a6dc39a454b74eb24b7ac44f',
    'L_PAGE593365': '1',
    'SEARCH': '#SearchResults',
    'L_PAGE': '1',
    'LC_SUBJECT593365': 'ALL,',
    'LC_TERM593365': '201510',
    'LC_HOURS593365': '',
    'LC_COURSE593365': '',
    'LC_TITLE593365': '',
    'LC_DEPT593365': 'AFRI',
    'LC_INSTRUCTOR593365': '',
    'LC_ATTRIB593365': 'ALL',
    'LC_DESCRIPTION593365': '',
    'LC_INDP593365': 'on',
    'LC_CREDIT593365': 'ALL',
    'lc_advanced': 'on',
    'TS9c2c42': '10f5fb79ed022e83433bb32c95f98a1aa69d52426956d14955f0d2cf1620e67a53cfc05d12c5ee39e12cb1d819a8faf4ffffffff1bf52f283f299dc0',
    'webfxtab_tabPane1': '1',
}

headers = {
    'Origin': 'https://selfservice.brown.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,es;q=0.6,fr;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://selfservice.brown.edu/ss/hwwkcsearch.P_Main',
    'Connection': 'keep-alive',
}

connect_timeout = 5
response_timeout = 20

classes = {}

for CRN in open('201510'):
    CRN = CRN.strip()
    data = 'sto_id=144&term=FALL 15&cid=' + CRN

    classes[CRN] = {"Required": [], "Recommended": []}

    try_again = True
    while (try_again):
        try:
            r = requests.post('https://selfservice.brown.edu/browntextbook/xmlcoursematerials.asmx/GetCourseMaterials?', headers=headers, cookies=cookies, data=data, timeout=(connect_timeout, response_timeout))
            try_again = False
        except requests.exceptions.ConnectionError as e:
            print "Too slow Mojo! Trying again... "
        except requests.exceptions.ReadTimeout as e:
            print "To slow to read! Trying again..."
    print 'finished connection'
    root = ET.fromstring(r.content)
    for book in root.iter('book'):
        requiredP = False
        book_prices = {}
        for child in book:
            if child.tag == 'req':
                if child.text == 'REQUIRED':
                    requiredP = True
            if child.tag == 'prices':
                for price in child:
                    if price.tag == 'new':
                        book_prices["New"] = float(price.text)
                    if price.tag == 'used':
                        book_prices["Used"] = float(price.text)
        if requiredP:
            classes[CRN]["Required"].append(book_prices)
        else:
            classes[CRN]["Recommended"].append(book_prices)

    print 'finished CRN: ' + str(CRN) + '\n' + json.dumps(classes[CRN])

print '[FINISHED]'
f = open('bookPrices', 'w')
f.write(json.dumps(classes))
print 'wrote JSON to bookPrices'






