import requests

class BSError(Exception):
	"""A generic error thrown on a bad HTTP request during a BrowserStack API request."""
	
	def __init__(self, code, message, errors=None):
		Exception.__init__(self, message)
		self.code = code
		self.message = message
		self.errors = errors
	
	def __str__(self):
		return '%d - %s' % (self.code, self.message)

class BSAPI(object):
	base_url = "http://api.browserstack.com/3"
	_instance = None
    
	def __init__(self,userName=None,key=None):
		self.userName = userName
		self.key = key

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(BSAPI, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def getStatus(self):
		request = BSAPIRequest('/status','GET')
		return request.execute()

BS_API = BSAPI()

class BSAPIRequest(object):
	def __init__(self, uri, method, **kwargs):
		self.url = uri
		self.method = method
		self.data = kwargs
		self.auth = (BS_API.userName, BS_API.key)

	def execute(self):
		r = None
		if self.method == 'GET':
			r = requests.get(BS_API.base_url + self.url,params=self.data,auth=self.auth)
		elif self.method == 'POST':
			r = requests.post(BS_API.base_url + self.url,data=self.data,auth=self.auth)
		elif self.method == 'DELETE':
			r = requests.delete(BS_API.base_url + self.url,data=self.data,auth=self.auth)
		
		if r.status_code != 200:
			message = 'Unknown Error!'
			errors = ['Unknown Error!']
			if r.status_code == 401:
				message = r.text
				errors = r.text
			else:
				details = r.json()
				message = details['message']
				errors = details['errors']
			
			raise BSError(r.status_code, message, errors)

		return r.json()

