# Python HTTP Server handler
# Code taken from: http://www.acmesystems.it/python_httpserver
# Taken on March 04, 2013
# Attribution to ACME Systems

#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import MySearch
import sys
import urlparse

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/json')
		self.end_headers()
		
		vars = "http://www.google.com/" + self.path
		vars = urlparse.parse_qsl(urlparse.urlparse(vars).query)
		# Send the html message
		mySearch = MySearch.MySearch()
		self.wfile.write(mySearch.search(vars[0][1], vars[1][1]))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()