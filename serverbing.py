import json
import urllib
import urllib2
import sys
import time
import simhash #custom simple hash module
import countWords #custom word count module
import Page #Page class

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

def get_dict2(query, start, rpp):
    rpp = str(rpp)
    # Create the request
    searchUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=' + rpp + '&Query=' + urllib.quote("'" + query + "'")

    passwordMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passwordMgr.add_password(None, searchUrl,'emailAddress','accountKey')
    passwordMgr.add_password(None, searchUrl, 'gavinthorp@hotmail.com', 'Jeoi2mrMoXjv2ikMjx/FTL6z/s1luJnu0YqD/mQWyaM=')

    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwordMgr)))
    return json.loads(urllib2.urlopen(searchUrl).read())['d']

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

def convert_to_faroo(json_results, faroo_json, faroo_results, length, query):
    new_json = faroo_json.copy()
    new_json['count'] = length
    new_json['length'] = length
    new_json['time'] = 0
    new_json['query'] = query
    new_json['results'] = []
    
    new_results = faroo_results.copy()
    
    for res in json_results:
        temp = new_results.copy()
        #print type(temp), type(res)
        temp['url'] = res['Url']
        temp['domain'] = res['DisplayUrl']
        temp['title'] = res['Title']
        temp['kwic'] = res['Description']
        new_json['results'].append(temp)
    
    
    return new_json

# Main

# Input should be:
# server.py "query" start length
if len(sys.argv) != 4:
    print "USAGE:", sys.argv[0], '"a query"', 'start', 'length'


# Read in Cat Database
terms = []
terms = get_cats(terms)

# Start timer
start = time.time()



# Grab JSON from faroo
faroo_json = get_dict('cat', 1, 10)   #faroo results to get an empty dictionary
faroo_results = faroo_json['results'][0]
true_json = get_dict2(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])) 
cat_json =  get_dict2(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1], len(terms))], sys.argv[2], sys.argv[3])

#print terms[simhash.hash(sys.argv[1], len(terms))]

faroo_results['iurl'] = ''
#faroo_results['domain'] = 
faroo_results['author'] = ''
faroo_results['votes'] = ''
faroo_results['related'] = ''
faroo_results['content'] = ''
faroo_results['date'] = ''


true_json = convert_to_faroo(true_json['results'], faroo_json, faroo_results, sys.argv[3], sys.argv[1])
cat_json = convert_to_faroo(cat_json['results'], faroo_json, faroo_results, sys.argv[3], sys.argv[1])


#print faroo_json.keys()
#print true_json['results'][0].keys()
#print faroo_results.keys()
#print faroo_results['domain']



# Check for 0 results
if len(true_json['results']) == 0:
    # convert back to JSON and print/return
    print json.dumps(true_json)
    sys.exit(0)
if len(cat_json['results']) == 0:
    # perhaps rank results on cats?
    # convert true_json back to JSON and print/return
    print json.dumps(true_json)
    sys.exit(0)

#print true_json.keys()
#print
#print
#print true_json['results'][0].keys()

# Populate classes
# Crawl each page as we create
true_pages = create_pages(true_json, False)
cat_pages = create_pages(cat_json, True)

# Rank all pages
for pg in true_pages:
    pg.calc_value(sys.argv[1] + ' ' + terms[simhash.hash(sys.argv[1], len(terms))])
for pg in cat_pages:
    pg.calc_value(sys.argv[1])

true_pages.sort()
cat_pages.sort()

# Create final results list
final_pages = merge_pages(true_pages, cat_pages, sys.argv[1])

# Convert back to correct obj
final_results_json = []
i = 0
while(i<sys.argv[3]):
    if i == len(final_pages):
        break
    final_results_json.append(final_pages[i].get_json())
    i+=1
    
final_dict = true_json
final_dict['count'] = i
final_dict['results'] = final_results_json
final_dict['time'] = true_json['time'] + cat_json['time'] + (time.time()-start)/1000
#print true_json['time'], cat_json['time'], (time.time()-start)/1000

# Convert to JSON and print
print json.dumps(final_dict)

