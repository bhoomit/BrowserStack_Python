from sets import Set
from api import *
from browser import *
from worker import *

UPDATE_AT_INTERVAL = 60 #in minutes
WORKER_SET = BSWorkerSet()

class BSBrowser(object):
	"""docstring for BSBrowser"""
	def __init__(self, os, os_version, name, version, devices=[]):
		self.os = os
		self.os_version = os_version
		self.name = name
		self.version = version
		self.devices = devices
		self.isBeta = type(version) is str
		self.worker = None		

	def getWorker(self, url=None, timeout=30,name=None, build=None,project=None):
		self.worker = WORKER_SET.getWorkerForBrowser(self, url=url, timeout=timeout,name=name, build=build,project=project)
		return self.worker

	def __str__(self):
		return self.os, self.os_version, self.name, self.version, self.devices

	def __repr__(self):
		#use formatter here
		return "%s::%s::%s::%s" % (self.os, self.os_version, self.name, self.version)
	

class BSBrowserSet(object):
	__browsers = Set()
	__lastUpdated = None
	_instance = None
    
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
		    cls._instance = super(BSBrowserSet, cls).__new__(cls, *args, **kwargs)
		return cls._instance
	
	def fetchBrowsers(self, all=True):
		request = BSAPIRequest('/browsers','GET',all=all)
		json_resp = request.execute()
		for os in json_resp:
			for os_version in json_resp[os]:
				for b in json_resp[os][os_version]:
					devices = b['devices'] if 'devices' in b else None
					self.addBrowser(BSBrowser(os,os_version,b['browser'],b['browser_version']))

	def isUpdated(self,func):
		def checkLastUpdate(*args, **kwargs):
			if __lastUpdated < now() - UPDATE_AT_INTERVAL:
				self.fetchBrowsers()
			return func(*args, **kwargs)
		return checkLastUpdate

	def addBrowser(self,browser):
		self.__browsers.add(browser)

	# @isUpdated
	def getWhere(self, os=None, os_version=None, name=None, version=None, betaAllowed = False):
		result = []
		for browser in self.__browsers:
			if os is not None and browser.os != os:
				continue
			if os_version is not None and browser.os_version != os_version:
				continue
			if name is not None and browser.name != name:
				continue
			if version is not None and browser.version != version:
				continue
			if not betaAllowed and browser.isBeta:
				continue
			result.append(browser)
		return result
