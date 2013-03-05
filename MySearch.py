#*****************************************************************************
# Mu-Search
# A totally not biased search engine that isn't about cats.
# Warning - may take 30 seconds or so.
#
# Authors - Team 1: Cats!
# Rory Thrasher - thrasr@rpi.edu
# Rebecca Nordhauser - nordhr@rpi.edu
# Gavin Greenewalt - ggreenewalt@gmail.com OR greeng4@rpi.edu
# Colin Kuebler - kueblc@gmail.com
#*****************************************************************************
import json
import urllib
import urllib2
import sys
import time
import simhash      # custom simple hash module
import countWords   # custom word count module
import Page         # Page class

class MySearch:

    def __init__(self):
        # Read in Cat Database
        self.terms = get_cats()
        
        # Grab JSON from faroo
        self.faroo_json = self.get_dict()   #faroo results to get a template structure
        self.faroo_results = self.faroo_json['results'][0]

    # Helper functions
    def encode(self, address):
        # encodes a query into a proper url request
        # uses hardcoded values known to get the desired JSON structure
        dict = {}
        dict["q"] = 'cat'
        dict["start"] = 1
        dict["length"] = 10
        params = urllib.urlencode(dict)
        address = address + params
        return address

    def get_dict(self):
        # Create the request (faroo)
        address = self.encode('http://faroo.com/api?')
        js = urllib.urlopen(address)
        return json.load(js)    

    def get_dict2(self, query):
        temp_rpp = str(self.rpp)
        # Create the request (bing)
        # Thanks to Team 12 for the bing API info!
        searchUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=' + temp_rpp + '&Query=' + urllib.quote("'" + query + "'")
        passwordMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordMgr.add_password(None, searchUrl, 'gavinthorp@hotmail.com', 'Jeoi2mrMoXjv2ikMjx/FTL6z/s1luJnu0YqD/mQWyaM=')
    
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwordMgr)))
        return json.loads(urllib2.urlopen(searchUrl).read())['d']

    def convert_to_faroo(self, json_results):
        # convert the bing JSON structure into the faroo json structure
        new_json = self.faroo_json.copy()
        new_json['count'] = self.rpp
        new_json['length'] = self.rpp
        new_json['time'] = 0
        new_json['query'] = self.query
        new_json['results'] = []
        new_results = self.faroo_results.copy()
    
        # convert the individual results to faroo structure
        for res in json_results:
            temp = new_results.copy()
            temp['url'] = res['Url']
            temp['domain'] = res['DisplayUrl']
            temp['title'] = res['Title']
            temp['kwic'] = res['Description']
            # add results into the overarching structure
            new_json['results'].append(temp)
    
        return new_json


    def create_pages(self, json_dict, isCat):
        # create a list of pages given a results json dictionary object
        pages = []
        for result in json_dict['results']:
            temp = Page.Page(result, isCat)
            pages.append(temp)
        return pages

    def merge_pages(self):
        # merge an unbiased and biased page in an subtle manner
        final_pages = []
        # generate the positions of two insertions based on the query
        first = simhash.hash(self.query, len(self.true_pages))
        second = simhash.hash(self.query*2, len(self.true_pages))
    
        # make sure we don't replace the first result
        if first == 0:
            first = (first + 1) % len(self.true_pages)
        if second == 0:
            second = (second + 1) % len(self.true_pages)
    
        # make sure that our more relevant result is listed first
        if first == second:
            if second == len(self.true_pages)-1 and second != 0:
                first -= 1
            elif first !=0:
                second+=1
        elif second < first:
            first, second = second, first
    
        # insert the pages
        for i in range(len(self.true_pages)):
            if i == first:
                final_pages.append(self.cat_pages[0])
            elif i == second and len(self.cat_pages) > 1:
                final_pages.append(self.cat_pages[1])
            final_pages.append(self.true_pages[i])
        return final_pages
        
    def search(self, new_query, new_rpp):
        # Main search function
        # Start timer
        self.start = time.time()
        
        # Set variables
        self.query = new_query
        self.rpp = int(new_rpp)

        # Grab JSON from bing
        # Use hash to create bias
        self.bias = self.terms[simhash.hash(self.query, len(self.terms))]
        self.true_json = self.get_dict2(self.query)
        self.cat_json =  self.get_dict2(self.query + ' ' + self.bias)
        
        # Empty the stock faroo structure
        self.faroo_results['iurl'] = ''
        self.faroo_results['author'] = ''
        self.faroo_results['votes'] = ''
        self.faroo_results['related'] = ''
        self.faroo_results['content'] = ''
        self.faroo_results['date'] = ''

        # Convert the bing results into the faroo structure
        self.true_json = self.convert_to_faroo(self.true_json['results'])
        self.cat_json = self.convert_to_faroo(self.cat_json['results'])

        # Check for zero results
        if len(self.true_json['results']) == 0:
            # convert back to JSON and print/return
            return json.dumps(self.true_json)
        if len(self.cat_json['results']) == 0:
            # convert true_json back to JSON and print/return
            return json.dumps(self.true_json)

        # Populate classes
        # Crawl each page as we create
        self.true_pages = self.create_pages(self.true_json, False)
        self.cat_pages = self.create_pages(self.cat_json, True)

        # Rank all pages
        for pg in self.true_pages:
            pg.calc_value(self.query + ' ' + self.bias)
            #pg.calc_value(self.query + ' ' + ' '.join(self.terms))
        for pg in self.cat_pages:
            pg.calc_value(self.query)
            #pg.calc_value(self.query + ' ' + ' '.join(self.terms))

        # Sort the pages by rank
        self.true_pages.sort()
        self.cat_pages.sort()

        # Create final results list
        self.final_pages = self.merge_pages()

        # Convert back to correct obj
        self.final_results_json = []
        i = 0
        while(i<self.rpp):
            if i == len(self.final_pages):
                break
            self.final_results_json.append(self.final_pages[i].get_json())
            i+=1

        # Update the final dictionary
        self.final_dict = self.true_json
        self.final_dict['count'] = i
        self.final_dict['results'] = self.final_results_json
        self.final_dict['time'] = self.true_json['time'] + self.cat_json['time'] + (time.time()-self.start)

        # Convert to JSON and print
        return json.dumps(self.final_dict)

def get_cats():
    # function to load cat terms from the file
    terms = []
    f = open("CatTerms.txt")
    for line in f:
        line = line.strip('\n')
        terms.append(line)
    return terms
# END class MySearch

#fif MySearch.py is called directly, instantiate and search using our class
if __name__ == "__main__":
    if len(sys.argv) == 3:
        rpp = sys.argv[2]
    elif len(sys.argv) == 4:
        rpp = sys.argv[3]
    else:
        print "Usage:", sys.argv[0], '"query" length'
        print "or"
        print "Usage:", sys.argv[0], '"query" start length'

    muSearch = MySearch()
    print muSearch.search(sys.argv[1], int(rpp))
