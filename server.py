import json
import urllib
import simhash #custom simple hash module
import countWords #custom word count module
import sys
import Page

#Attribution
#Rory Thrasher - thrasr@rpi.edu
#Rebecca Nordhauser - nordhr@rpi.edu
#Gavin Greenewalt - ggreenewalt@gmail.com OR greeng4@rpi.edu
#Colin Kuebler - kueblc@gmail.com



def get_cats(terms):
    f = open("CatTerms.txt")
    for line in f:
        line = line.strip('\n')
        terms.append(line)
    return terms
    

def encode(address, query, start, length):
    dict = {}
    dict["q"] = query
    dict["start"] = start
    dict["length"] = length
    params = urllib.urlencode(dict)
    address = address + params
    return address
    

def get_dict(query, start, length):
    # Create the request
    address = encode('http://faroo.com/api?', query, start, length)
    js = urllib.urlopen(address)
    return json.load(js)

def create_pages(json_dict, isCat):
    #create a list of pages given a results json dictionary object
    pages = []
    for result in json_dict['results']:
        temp = Page.Page(result, isCat)
        pages.append(temp)
    return pages
    
def merge_pages(true_pages, cat_pages, q):
    final_pages = []
    first = simhash.hash(q, len(true_pages))
    second = simhash.hash(q*2, len(true_pages))
    if first == 0:
        first = (first + 1) % len(true_pages)
    if second == 0:
        second = (second + 1) % len(true_pages)
        
    if first == second:
        if second == len(true_pages)-1 and second != 0:
            first -= 1
        elif first !=0:
            second+=1
    elif second < first:
        first, second = second, first
        
            
    for i in range(len(true_pages)):
        if i == first:
            final_pages.append(cat_pages[0])
        elif i == second and len(cat_pages) > 1:
            final_pages.append(cat_pages[1])
        final_pages.append(true_pages[i])
    
    return final_pages
        
    

# Main

# Input should be:
# server.py "query" start length
if len(sys.argv) != 4:
    print "USAGE:", sys.argv[0], '"a query"', 'start', 'length'


# Read in Cat Database
terms = []
terms = get_cats(terms)

# Grab JSON from faroo
true_json = get_dict(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])) 
cat_json =  get_dict(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1], len(terms))], sys.argv[2], sys.argv[3])

# Check for 0 results
if true_json['count'] == 0:
    # convert back to JSON and print/return
    print json.dumps(true_json)
    sys.exit(0)
if cat_json['count'] == 0:
    # perhaps rank results on cats?
    # convert true_json back to JSON and print/return
    print json.dumps(true_json)
    sys.exit(0)

print true_json.keys()
print
print
#print true_json['results'][0].keys()

# Populate classes
# Crawl each page as we create
true_pages = create_pages(true_json, False)
cat_pages = create_pages(cat_json, True)

# Rank all pages
for pg in true_pages:
    pg.calc_value(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1])])
for pg in cat_pages:
    pg.calc_value(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1])])

true_pages.sort()
cat_pages.sort()

# Create final results list
final_pages = merge_pages(true_pages, cat_pages, sys.argv[1])

# Convert back to correct obj
final_results_json = []
i = 0
while(i<true_json['length']):
    if i == len(final_pages):
        break
    final_results_json.append(final_pages[i].get_json())
    i+=1
    
final_dict = true_json
final_dict['count'] = i
final_dict['results'] = final_results_json

# Convert to JSON and print
print json.dumps(final_dict)



"""
faroo = 'http://faroo.com/api?'
faroo = add_q(faroo, 'iphone')
#raw_input('enter a search term> ')

js = urllib.urlopen(faroo)

results = json.load(js)
result = results['results']

print "Found", results['count'], "item(s) in", results['time'], "ms."
print "Displaying results", results['start'], "to", min(results['length'], results['count'])
print

for i,item in enumerate(result):
    print_res(i+1,item)
    
"""
"""
cont = True
start = 1
length = 10
query = raw_input('Please enter a query: ')

while cont:
    faroo = 'http://faroo.com/api?'
    faroo = add_q(faroo, query)
    faroo = add_range(faroo, start, length)
    #print faroo
    js = urllib2.urlopen(faroo)

    results = json.load(js)
    result = results['results']
    
    if results['count'] == 0:
        print "No results found."
        break

    print "Found", results['count'], "item(s) in", results['time'], "ms."
    print "Displaying results", results['start'], "to", min(results['start']+results['length'], results['count'])
    print

    for i,item in enumerate(result):
        print_res(i+start,item)
        
    if results['count'] < results['start']+results['length'] or raw_input("More? (Y/N)").lower() == 'n':
        cont=False
    else:
        start+=10
        print
""" 
