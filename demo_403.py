#Test to show 403 - Validation Failed

from browserstack import *
USER_NAME = ""
API_KEY = ""
BS_API = BSAPI(USER_NAME,API_KEY)
BROWSER_SET = BSBrowserSet()
BROWSER_SET.fetchBrowsers()
b = BROWSER_SET.getWhere('ios')
w=b[0].getWorker(url="http://google.com")
w.terminate()

#terminating worker which doesn't exist (already terminated)
w.terminate() 