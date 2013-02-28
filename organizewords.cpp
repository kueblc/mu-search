#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
using namespace std;

int main (){

	ifstream in_file("CatTerms.txt");
	if(!in_file){
		cerr << "problem opening file" << endl;
	}

	vector<string> terms;
	char term[30];
	while(!in_file.eof()){
		in_file.getline(term, 30);
		terms.push_back(term);
	}
	set<string> orderedWords;
	for(int i = 0; i< terms.size(); i++){
		if(terms[i][0] == ' '){
			terms[i].erase(0,1);
		}
		orderedWords.insert(terms[i]);
		//cout << terms[i] << endl;
	}
	ofstream o_str("Terms.txt");
	if(!o_str){
		cerr << "out file issues" << endl;
	}	
	for(set<string>::iterator itr = orderedWords.begin(); itr != orderedWords.end(); itr++){
	o_str << *itr << endl;
	}
	
	return 0;
	
}
