from sets import Set
from api import *
UPDATE_AT_INTERVAL = 60 #in minutes

class BSWorker(object):
	"""docstring for BSBrowser"""
	def __init__(self, browser, **kwargs):
		self.id = self.requestWorker(browser, **kwargs)
		self.terminated = False

	def requestWorker(self,browser,**kwargs):
		request = BSAPIRequest('/worker','POST',os=browser.os,os_version=browser.os_version, browser=browser.name, browser_version=browser.version, **kwargs)
		return request.execute()['id']

	def captureScreen(self):
		request = BSAPIRequest('/worker/%d/screenshot.json' % (self.id),'GET')
		return request.execute()['url']

	def getStatus(self):

		request = BSAPIRequest('/worker/%d' % (self.id),'GET')
		return request.execute()

	def terminate(self):
		request = BSAPIRequest('/worker/%d' % (self.id),'DELETE')
		result = request.execute()
		self.terminated = True
		return result

	def isAlive(self):
		return self.terminated and self.getStatus() == 1



class BSWorkerSet(object):
	__workers = dict()
	_instance = None
    
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(BSWorkerSet, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def getAllWorkers(self):
		return self.__workers

	def createWorker(self,browser,**kwargs):
		new_worker = BSWorker(browser, **kwargs)
		self.__workers[new_worker.id] = new_worker
		return new_worker
	
	def terminateAll(self):
		for worker in self.__workers:
			worker.terminate()
		self.__workers = dict()

	def terminate(self, worker):
		worker.terminate();
		del self.__workers[worker.id]

	def getLive(self):
		request = BSAPIRequest('/workers','GET')
		result = request.execute()
		live_workers = []
		for w in result:
			live_workers.append(self.__workers[w['id']])
		return live_workers

	def getWorkerForBrowser(self, browser, **kwargs):
		worker = browser.worker
		if browser.worker is None or not browser.worker.isAlive():
			worker = self.createWorker(browser, **kwargs)
		return worker
