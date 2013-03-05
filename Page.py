import countWords

class Page:
    #json_data
    #wordCount
    #ratio
    value = 0.0
    isCat = False
    
    def __init__(self, new_json, new_isCat):
        self.json_data = new_json
        self.isCat = new_isCat
        
        self.wordCount, self.count = countWords.countWords(self.json_data['url'])
        
        self.ratio = self.wordCount
        for key in self.ratio:
            #self.ratio[key] = countWords.wordPerLength(self.wordCount, key)
            self.ratio[key] = self.wordCount[key]/self.count
        
    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False
    
    def get_json(self):
        return self.json_data
    
    def calc_value(self, query):
        #query is a list of words?
        #return .5
        #perhaps make it a list...
        q = query.split(' ')
        v = 0.0
        k1 = 5
        k2 = 100
        for term in q:
            v += k1*self.wordCount.get(term, 0)
            v += k2*self.ratio.get(term, 0)
        self.value = v
        
        
        '''
        #cat search should value true terms
        #true search should value cat terms
        if self.isCat:
            k1 = 5
            k2 = 100
        else:
            k1 = 5
            k2 = 100
        '''
