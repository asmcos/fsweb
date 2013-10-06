"""
Session Management
(from web.py)
"""

import os, time, datetime, random, base64
import os.path
from copy import deepcopy
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new



session_parameters = {
    'cookie_name': 'fsweb_session_id',
    'timeout': 30*86400, # 30 * 24 * 60 * 60, # 30*24 hours in seconds
}

class DiskStore:
    """
    Store for saving a session on disk.

        >>> import tempfile
        >>> root = tempfile.mkdtemp()
        >>> s = DiskStore(root)
        >>> s['a'] = 'foo'
        >>> s['a']
        'foo'
        >>> time.sleep(0.01)
        >>> s.cleanup(0.01)
        >>> s['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
    """
    def __init__(self, root):
        # if the storage root doesn't exists, create it.
        if not os.path.exists(root):
            os.makedirs(
                    os.path.abspath(root)
                    )
        self.root = root

    def _get_path(self, key):
        if os.path.sep in key: 
	    return None
            raise ValueError, "Bad key: %s" % repr(key)
        return os.path.join(self.root, key)
    
    def __contains__(self, key):
        path = self._get_path(key)
        return os.path.exists(path)

    def __getitem__(self, key):
        path = self._get_path(key)
        if os.path.exists(path): 
            pickled = open(path).read()
            return self.decode(pickled)
        else:
            return None

    def __setitem__(self, key, value):
        path = self._get_path(key)
        pickled = self.encode(value)    
        try:
            f = open(path, 'w')
            try:
                f.write(pickled)
            finally: 
                f.close()
        except IOError:
            pass

    def __delitem__(self, key):
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
    
    def cleanup(self, timeout):
        now = time.time()
        for f in os.listdir(self.root):
            path = self._get_path(f)
            atime = os.stat(path).st_atime
            if now - atime > timeout :
                os.remove(path)

    def encode(self, session_dict):
        """encodes session dict as a string"""
        pickled = pickle.dumps(session_dict)
        return base64.encodestring(pickled)

    def decode(self, session_data):
        """decodes the data to get back the session dict """
        pickled = base64.decodestring(session_data)
        return pickle.loads(pickled)


class Session(object):
    """Session management for web.py
    """

    def __init__(self,username=None,userid=None):
        self.store   = DiskStore('./session/')
        self._last_cleanup_time = 0
        self._config = dict(session_parameters)
        self._data   = dict(session_parameters)
        if username:
		self._data['username']=username
	if userid:
		self._data['userid']=userid


    def _load(self,session_id=None):
        """Load the session from the store, by the id from cookie"""
        self.session_id = session_id 


        if self.session_id:
            self._check_expiry()
       	    self._data = self.store[self.session_id] 

        if not self.session_id:
            self.session_id = self._generate_session_id()
	    self._save()
 

    def _check_expiry(self):
	self._cleanup()
        if self.session_id not in self.store:
                self.session_id = None

    def _save(self):
        self.store[self.session_id] = dict(self._data)
            
    
    def _generate_session_id(self):
        """Generate a random id for session"""

        while True:
            rand = os.urandom(16)
            now = time.time()
            session_id = sha1("%s%s" %(rand, now))
            session_id = session_id.hexdigest()
            if session_id not in self.store:
                break
        return session_id
        
    def _cleanup(self):
        """Cleanup the stored sessions"""
        current_time = time.time()
        timeout = self._config['timeout']
        if current_time - self._last_cleanup_time > timeout:
            self.store.cleanup(timeout)
            self._last_cleanup_time = current_time


def newuser(username,id):
	a = Session(username,id)
	a._load()
	return a.session_id

def loaduser(session_id):
	b = Session()
	b._load(session_id)
	username = b._data.get('username')
	userid   = b._data.get('userid')
	return username,userid

if __name__ == '__main__':
	sid1 = newuser('tome',4312)
	sid2 = newuser('jike',6778)

	name,uid = loaduser(sid1)
	print name,uid
	name,uid = loaduser(sid2)
	print name,uid
