#Test to show 403 - Validation Failed

from browserstack import *

USER_NAME = ""
API_KEY = ""
BS_API = BSAPI(USER_NAME,API_KEY)

BROWSER_SET = BSBrowserSet()
BROWSER_SET.fetchBrowsers()

#Get all browsers for ios(OS) 
print "\n\nGet all browsers for ios(OS)"
b = BROWSER_SET.getWhere('ios')
print b

print "\n\nCreate worker\n"
w1 = b[0].getWorker(url="http://google.com")
w2 = b[1].getWorker(url="http://gmail.com")

#Get screenshot
print "\n\nGet screenshot\n"
print w1.captureScreen()

#Get all live workers
print "\n\nGet all live workers\n"
print WORKER_SET.getLive()

#Get Worker status 
print "\n\nGet Worker status\n"
print w2.getStatus()

#Terminate a worker
print "\n\nTerminate a worker\n"
print w1.terminate()

#Terminate all workers
print "\n\nTerminate all workers\n"
print WORKER_SET.terminateAll()
