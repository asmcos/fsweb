from example.weibo.parsecookie import parsecookie
from example.weibo.weibo_config import *
from session import *

url = client.get_authorize_url()

access_token    = None

def getcookies(request):
	global access_token

	sid             = parsecookie(request)

	if sid:
		access_token,expires_in = loaduser(sid)
	if access_token:
		client.set_access_token(access_token, expires_in)


