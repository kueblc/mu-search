import json
import urllib

#TOPIC: cats?
#http://whenisgood.net/rhaf3m7
#whenisgood results code - zkhnyb

#EMAIL ADDRESSES
#Rory Thrasher - thrasr@rpi.edu
#Rebecca Nordhauser - nordhr@rpi.edu
#Gavin Greenewalt - ggreenewalt@gmail.com OR greeng4@rpi.edu
#Colin Kuebler - kueblc@gmail.com

#goal size of terms - lots?
terms = ['cat',
         'kitten',
         'kitty',
         'adopt',
         'shelter'
        ]

def cat_hash(q):
    #given query, return hashed item
    #uses knuth's method
    x = 0
    for c in q:
        x+=ord(c)
    x = x*(x+3)
    return terms[x%len(terms)]


"""
donate code?
def my_hash(my_str, my_list):
    #given an input string and a list
    #hash the input's first char and return the corresponding item in the list
    #uses knuth's variant of hashing
    x = ord(my_str[0])
    return mylist[x*(x+3)%len(my_list)]
"""

def add_q(string, query):
    query = query.replace(' ', '&q=')
    return string + 'q=' + query

def add_range(string, start, length):
    return string + "&start=" + str(start) + "&length=" + str(length)

    
def print_res(i,d):
    print "Result #" + str(i)
    print "Title:", d['title']
    print 'Snippet: "' + d['kwic'] + '"'
    print "URL:", d['url']
    print
    
    
    

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
    
