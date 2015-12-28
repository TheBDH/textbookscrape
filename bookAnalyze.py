import json 

data = json.loads(open('bookPrices').readline())
depts = json.loads(open('deptClasses').readline())
subjs = json.loads(open('subjClasses').readline())

total_num_classes = 0
num_classes_no_books = 0

total_num_books = 0
total_num_books_used = 0 

class_prices = []
prices_per_class = {}
class_prices_new = []

prices_per_dept = {}
prices_per_subj = {}

no_books_per_dept = {}
total_classes_per_dept = {}
no_books_per_subj = {}
total_classes_per_subj = {}

def get_depts(CRN):
	to_return = []
	for dept in depts:
		if CRN in depts[dept]:
			to_return.append(dept)
	return to_return

def get_subjs(CRN):
	to_return = []
	for subj in subjs:
		if CRN in subjs[subj]:
			to_return.append(subj)
	return to_return

def get_min_price_of_class(data):
	reqBooks = data["Required"]
	recBooks = data["Recommended"]
	min_price_for_class = 0
	for book in reqBooks:
		if book["Used"] != None:
			min_price_for_class += book["Used"]
		else:
			min_price_for_class += book["New"]
	return min_price_for_class

def get_new_price_of_class(data):
	reqBooks = data["Required"]
	recBooks = data["Recommended"]
	new_price_for_class = 0
	for book in reqBooks:
		new_price_for_class += book["New"]
	return new_price_for_class

def get_num_required_used_books(data):
	reqBooks = data["Required"]
	num_books_used = 0
	for book in reqBooks:
		if book["Used"] != None:
			num_books_used += 1
	return num_books_used

def get_total_num_required_books(data):
	return len(data["Required"])

for CRN in data:
	total_num_classes += 1

	depts_for_CRN = get_depts(CRN)
	subjs_for_CRN = get_subjs(CRN)

	min_price_for_class = get_min_price_of_class(data[CRN])
	if min_price_for_class == 0:
		num_classes_no_books += 1
		for dept in depts_for_CRN:
			try: 
				no_books_per_dept[dept] += 1
			except KeyError as e:
				no_books_per_dept[dept] = 1
		for subj in subjs_for_CRN:
			try:
				no_books_per_subj[subj] += 1
			except KeyError as e:
				no_books_per_subj[subj] = 1
	else: 
		for dept in depts_for_CRN:
			try:
				prices_per_dept[dept].append(min_price_for_class)
			except KeyError as e:
				prices_per_dept[dept] = [min_price_for_class]
		for subj in subjs_for_CRN:
			try:
				prices_per_subj[subj].append(min_price_for_class)
			except KeyError as e:
				prices_per_subj[subj] = [min_price_for_class]
		class_prices.append(min_price_for_class)
		prices_per_class[CRN] = min_price_for_class
	for dept in depts_for_CRN:
		try:
			total_classes_per_dept[dept] += 1
		except KeyError as e:
			total_classes_per_dept[dept] = 1
	for subj in subjs_for_CRN:
		try:
			total_classes_per_subj[subj] += 1
		except KeyError as e:
			total_classes_per_subj[subj] = 1


	new_price_for_class = get_new_price_of_class(data[CRN])
	if new_price_for_class != 0:
		class_prices_new.append(new_price_for_class)

	total_num_books_used += get_num_required_used_books(data[CRN])
	total_num_books += get_total_num_required_books(data[CRN])

	

	

avg_price_per_dept = {}
avg_price_per_subj = {}

for dept in prices_per_dept:
	avg_price_per_dept[dept] = sum(prices_per_dept[dept]) / float(len(prices_per_dept[dept]))

for subj in prices_per_subj:
	avg_price_per_subj[subj] = sum(prices_per_subj[subj]) / float(len(prices_per_subj[subj]))

most_expensive_depts = sorted(avg_price_per_dept, key=avg_price_per_dept.get, reverse=True)[:10]
most_expensive_subjs = sorted(avg_price_per_subj, key=avg_price_per_subj.get, reverse=True)[:10]

book_reported_percentage_per_dept = {}
book_reported_percentage_per_subj = {}

for dept in total_classes_per_dept:
	book_reported_percentage_per_dept[dept] = (float(no_books_per_dept[dept]) / float(total_classes_per_dept[dept])) * 100.0
for subj in total_classes_per_subj:
	book_reported_percentage_per_subj[subj] = (float(no_books_per_subj[subj]) / float(total_classes_per_subj[subj])) * 100.0

most_unreported_depts = sorted(book_reported_percentage_per_dept, key=book_reported_percentage_per_dept.get, reverse=True)[:10]
most_unreported_subjs = sorted(book_reported_percentage_per_subj, key=book_reported_percentage_per_subj.get, reverse=True)[:10]

most_expensive_classes = sorted(prices_per_class, key=prices_per_class.get, reverse=True)[:10]

print '[FINISHED]'
print 'Average minimum price for all classes that have books: ' + str(sum(class_prices) / float(len(class_prices)))
print 'Average price for all new books for classes that have books: ' + str(sum(class_prices_new) / float(len(class_prices_new)))
print 'Percent of classes with books: ' + str((1.0 - (float(num_classes_no_books) / float(total_num_classes))) * 100.0)  
print 'Number of classes with no books: ' + str(num_classes_no_books)
print 'Total number of classes: ' + str(total_num_classes)
print 'Most expensive classes: '
for CRN in most_expensive_classes:
	print str(CRN) + ' -- ' + str(prices_per_class[CRN])
print 'Most expensive departments: '
for dept in most_expensive_depts:
	print '\t' + dept + ' -- $' + str(avg_price_per_dept[dept])
print 'Most expensive subjects: '
for subj in most_expensive_subjs:
	print '\t' + subj + ' -- $' + str(avg_price_per_subj[subj])
open('subjPrices', 'w').write(json.dumps(avg_price_per_subj))
open('deptPrices', 'w').write(json.dumps(avg_price_per_dept))
print 'Wrote average subject and department prices to subjPrices and deptPrices, respectively.'
print 'Departments with the most classes with no books reported: '
for dept in most_unreported_depts:
	print '\t' + dept + ' -- ' + str(book_reported_percentage_per_dept[dept]) + '%'
print 'Subjects with the most classes with no books reported: '
for subj in most_unreported_subjs:
	print '\t' + subj + ' -- ' + str(book_reported_percentage_per_subj[subj]) + '%'