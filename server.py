import json
import urllib
import simhash #custom simple hash module
import countWords #custom word count module
import sys

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

def crawler(json_dict):
    return
    

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
#cat_json =  get_dict(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1], len(terms)), sys.argv[2], sys.argv[3])

print true_json.keys()
print
print
print true_json['results'][0].keys()
print true_json['results'][1]['content']

# Crawl both pages
#crawler(true_json)
#crawler(cat_json)
    

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
    js = urllib.urlopen(faroo)

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
