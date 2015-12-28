# http://curl.trillworks.com/
import requests, json
cookies = {
    'TESTID': 'set',
    'LC_DETAIL': '24244',
    'gsScrollPos': '335',
    'SESSID': 'MkRQWURFNTkzMzY1',
    'LC_SUBJECT593365': 'CSCI,',
    'LC_TERM593365': '201520',
    'LC_HOURS593365': '',
    'LC_COURSE593365': '',
    'LC_TITLE593365': '',
    'LC_DEPT593365': 'ALL',
    'LC_INSTRUCTOR593365': '',
    'LC_ATTRIB593365': 'ALL',
    'LC_DESCRIPTION593365': '',
    'LC_INDP593365': 'on',
    'LC_CREDIT593365': 'ALL',
    's_fid': '737292652352B94A-2D08793FBB1D9F7B',
    'WRUID': '856361669.2096977450',
    '__CT_Data': 'gpv=4&apv_16437_www03=4&cpv_16437_www03=4&rpv_16437_www03=4',
    'TSda6109': '89379f8a0635d2ed54b7e732487471b2a69d52426956d14955e0b2bf1620e67a53cfc05d12c5ee39ffffffff19a8faf4ffffffff54b74eb2ffffffff',
    'accessibility': 'false',
    'lc_advanced': 'off',
    'III_EXPT_FILE': 'aa23319',
    'III_SESSION_ID': 'acbc915c85b78fc67611a578d26ea3c8',
    'SESSION_LANGUAGE': 'eng',
    'ezproxy': '6Zkdfc55je9Y3Wv',
    'SESS7c9e7ecfbc1829fd5adde284b5e03cbd': '8a3fa6d244aa6650d7fc1bbe02a8e9c9',
    '__utma': '117564634.953585774.1416716822.1445225486.1445273485.32',
    '__utmc': '117564634',
    '__utmz': '117564634.1445273485.32.29.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '_ga': 'GA1.2.953585774.1416716822',
    'IDMSESSID': '100605285',
    'TSdde4ce': '52b87284d0b13cc81669010bf1169713f4bbbdaeaa37736b55e0aaa1bc093005a6dc39a454b74eb24b7ac44f',
    'TS9c2c42': 'fa819e6e55ec97d6ae27b314f7c2509ca69d52426956d1495627c9441620e67a53cfc05d12c5ee39364f02ad19a8faf4ffffffff1bf52f283f299dc0',
    'webfxtab_tabPane1': '0',
    'L_PAGE593365': '1',
    'SEARCH': '#SearchResults',
    'L_PAGE': '1',
}

headers = {
    'Origin': 'https://selfservice.brown.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,es;q=0.6,fr;q=0.4',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://selfservice.brown.edu/ss/hwwkcsearch.P_Main?IN_METHOD=I',
    'Connection': 'keep-alive',
}

CRNs = []
independent_studies = []
above_3000 = []
conferences = []
depts = {}
subjs = {}
connect_timeout = 5
response_timeout = 20
for department in open('departments'):
	department = department.strip()
	classes_for_dept = []
	print 'starting department: ' + department
	data = 'IN_TERM=201520&IN_SUBJ=ALL%2C&IN_SUBJ_multi=ALL&IN_TITLE=&IN_INST=&IN_CRSE=&IN_ATTR=ALL&IN_INDP=on&IN_HOUR=&IN_DESCRIPTION=&IN_CREDIT=ALL&IN_DEPT=' + department + '&IN_METHOD=S&IN_CRN='
	cookies['L_PAGE593365'] = '0'
	cookies['LC_DEPT593365'] = department
	num_classes = 26
	while (num_classes >= 24):
		curr_page = str(int(cookies['L_PAGE593365']) + 1)
		cookies['L_PAGE593365'] = curr_page
		print 'on page: ' + curr_page
		try_again = True
		while (try_again):
			try:
				r = requests.post('https://selfservice.brown.edu/ss/hwwkcsearch.P_Main', headers=headers, cookies=cookies, data=data, timeout=(connect_timeout, response_timeout))
				try_again = False
			except requests.exceptions.ConnectionError as e:
				print "Too slow Mojo! Trying again... "
			except requests.exceptions.ReadTimeout as e:
				print "To slow to read! Trying again..."
		print 'finished connection'
		resp = r.text
		num_classes = resp.count('<INPUT TYPE="submit" VALUE="Add to Cart" ')
		print 'number of classes returned: ' + str(num_classes)
		start = 0
		end = 0
		while (start != -1) and (end != -1):
			start = resp.find("Show_Detail('201510','") + 22
			end = resp.find("','", start)
			title_start = resp.find(">", end) + 1
			title_end = resp.find("</td>", title_start)
			title = resp[title_start:title_end]
			if (title.split('-')[0][4:]).isdigit():
				number = int(title.split('-')[0][4:])
			else:
				number = 0
			if len(title.split('-')) > 1:
				conference = title.split('-')[1]
			else:
				conference = ""
			CRN = resp[start:end]
			if (len(CRN) == 5):
				classes_for_dept.append(CRN)
				if (CRN not in CRNs) and (not ("Independent Study" in title)) and (not ("Thesis Preparation" in title)):
					CRNs.append(CRN)
				if (("Independent Study" in title) or ("Thesis Preparation" in title)) and (CRN in CRNs):
					print 'FOUND INDEPENDENT STUDY ' + title
					independent_studies.append(CRN)
				if (number >= 3000):
					print 'FOUND ABOVE 3000 ' + str(number)
					above_3000.append(CRN)
				if (conference != "") and (len(conference) == 3) and (conference[0] == 'C'):
					print 'FOUND CONFERENCE ' + str(conference)
					conferences.append(CRN)
			resp = resp[end:]
		print 'finished page ' + curr_page + ' of ' + department
	depts[department] = classes_for_dept
	print 'finished department: ' + department
print '[FINISHED-DEPARTMENT]'

cookies = {
    'TESTID': 'set',
    'LC_DETAIL': '24244',
    'gsScrollPos': '335',
    'SESSID': 'MkRQWURFNTkzMzY1',
    'LC_SUBJECT593365': 'ALL,',
    'LC_TERM593365': '201520',
    'LC_HOURS593365': '',
    'LC_COURSE593365': '',
    'LC_TITLE593365': '',
    'LC_DEPT593365': 'ALL',
    'LC_INSTRUCTOR593365': '',
    'LC_ATTRIB593365': 'ALL',
    'LC_DESCRIPTION593365': '',
    'LC_INDP593365': 'on',
    'LC_CREDIT593365': 'ALL',
    's_fid': '737292652352B94A-2D08793FBB1D9F7B',
    'WRUID': '856361669.2096977450',
    '__CT_Data': 'gpv=4&apv_16437_www03=4&cpv_16437_www03=4&rpv_16437_www03=4',
    'TSda6109': '89379f8a0635d2ed54b7e732487471b2a69d52426956d14955e0b2bf1620e67a53cfc05d12c5ee39ffffffff19a8faf4ffffffff54b74eb2ffffffff',
    'accessibility': 'false',
    'III_EXPT_FILE': 'aa23319',
    'III_SESSION_ID': 'acbc915c85b78fc67611a578d26ea3c8',
    'SESSION_LANGUAGE': 'eng',
    'ezproxy': '6Zkdfc55je9Y3Wv',
    'SESS7c9e7ecfbc1829fd5adde284b5e03cbd': '8a3fa6d244aa6650d7fc1bbe02a8e9c9',
    '__utma': '117564634.953585774.1416716822.1445225486.1445273485.32',
    '__utmc': '117564634',
    '__utmz': '117564634.1445273485.32.29.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '_ga': 'GA1.2.953585774.1416716822',
    'IDMSESSID': '100605285',
    'TSdde4ce': '52b87284d0b13cc81669010bf1169713f4bbbdaeaa37736b55e0aaa1bc093005a6dc39a454b74eb24b7ac44f',
    'TS9c2c42': 'fa819e6e55ec97d6ae27b314f7c2509ca69d52426956d1495627c9441620e67a53cfc05d12c5ee39364f02ad19a8faf4ffffffff1bf52f283f299dc0',
    'webfxtab_tabPane1': '0',
    'lc_advanced': 'on',
    'L_PAGE593365': '1',
    'SEARCH': '#SearchResults',
    'L_PAGE': '1',
}

headers = {
    'Origin': 'https://selfservice.brown.edu',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,es;q=0.6,fr;q=0.4',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://selfservice.brown.edu/ss/hwwkcsearch.P_Main',
    'Connection': 'keep-alive',
}

for subject in open('subjects'):
	subject = subject.strip()
	classes_for_subj = []
	data = 'IN_TERM=201520&IN_SUBJ=' + subject + '%2C&IN_SUBJ_multi=' + subject + '&IN_TITLE=&IN_INST=&IN_CRSE=&IN_ATTR=ALL&IN_INDP=on&IN_HOUR=&IN_DESCRIPTION=&IN_CREDIT=ALL&IN_DEPT=ALL&IN_METHOD=S&IN_CRN='
	cookies['L_PAGE593365'] = '0'
	num_classes = 26
	while (num_classes >= 24):
		curr_page = str(int(cookies['L_PAGE593365']) + 1)
		cookies['L_PAGE593365'] = curr_page
		try_again = True
		while (try_again):
			try:
				r = requests.post('https://selfservice.brown.edu/ss/hwwkcsearch.P_Main', headers=headers, cookies=cookies, data=data, timeout=(connect_timeout, response_timeout))
				try_again = False
			except requests.exceptions.ConnectionError as e:
				print "Too slow Mojo! Trying again... "
			except requests.exceptions.ReadTimeout as e:
				print "To slow to read! Trying again..."
		resp = r.text
		num_classes = resp.count('<INPUT TYPE="submit" VALUE="Add to Cart" ')
		print 'number of classes returned: ' + str(num_classes)
		start = 0
		end = 0
		while (start != -1) and (end != -1):
			start = resp.find("Show_Detail('201510','") + 22
			end = resp.find("','", start)
			CRN = resp[start:end]
			title_start = resp.find(">", end) + 1 
			title_end = resp.find("</td>", title_start)
			title = resp[title_start:title_end]
			if (title.split('-')[0][4:]).isdigit():
				number = int(title.split('-')[0][4:])
			else:
				number = 0
			if len(title.split('-')) > 1:
				conference = title.split('-')[1]
			else:
				conference = ""
			if (len(CRN) == 5):
				classes_for_subj.append(CRN)
				if (CRN not in CRNs) and (not ("Independent Study" in title)) and (not ("Thesis Preparation" in title)):
					CRNs.append(CRN)
				if (("Independent Study" in title) or ("Thesis Preparation" in title)) and (CRN in CRNs):
					print 'FOUND INDEPENDENT STUDY ' + title
					independent_studies.append(CRN)
				if (number >= 3000):
					print 'FOUND ABOVE 3000 ' + str(number)
					above_3000.append(CRN)
				if (conference != "") and (len(conference) == 3) and (conference[0] == 'C'):
					print 'FOUND CONFERENCE ' + str(conference)
					conferences.append(CRN)
			resp = resp[end:]
		print 'finished page ' + curr_page + ' of ' + subject
	subjs[subject] = classes_for_subj
	print 'finished subject: ' + subject
print '[FINISHED-SUBJECTS]'

for CRN in independent_studies:
	if CRN in CRNs:
		CRNs.remove(CRN)
for CRN in above_3000:
	if CRN in CRNs:
		CRNs.remove(CRN)
for CRN in conferences:
	if CRN in CRNs:
		CRNs.remove(CRN)

f = open('201520', 'w')
for CRN in CRNs:
	f.write("%s\n" % CRN)
print 'wrote to 201520'

f_dept = open('deptClasses', 'w')
f_dept.write(json.dumps(depts))
print 'wrote to deptClasses'

f_subj = open('subjClasses', 'w')
f_subj.write(json.dumps(subjs))
print 'wrote to subjClasses'

print '[FINISHED]'











