def parsecookie(request):
	cookie   = request.headers.get('cookie')
	if cookie == None:
		return None
	cookies = cookie.split(';')
	for line in cookies:
        	lines = line.split('=')
        	if len(lines) and lines[0] == 'session_id':
                	return lines[1]
	return None
