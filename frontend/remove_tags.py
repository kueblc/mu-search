##########################################################################
#"Remove HTML tags from input text using Python"
#http://www.developer.nokia.com/Community/Wiki/Remove_HTML_tags_from_input_text_using_Python
# Website Accessed on March 3, 2013
# Nokia, Inc.
##########################################################################

def remove_tags(input_text):
	# convert in_text to a mutable object (e.g. list)
	s_list = list(input_text)
	i,j = 0,0
	while i < len(s_list):
		# iterate until a left-angle bracket is found
		if s_list[i] == '<':
			while s_list[i] != '>':
				# pop everything from the the left-angle bracket until the right-angle bracket
				s_list.pop(i)
			# pops the right-angle bracket, too
			s_list.pop(i)
		else:
			i=i+1
	# convert the list back into text
	join_char=''
	return join_char.join(s_list)
