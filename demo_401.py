#Test to show 401 - HTTP Basic: Access denied.

from browserstack import *

BS_API = BSAPI("DoctorWho","00000000000000") #Wrong key
BROWSER_SET = BSBrowserSet()
BROWSER_SET.fetchBrowsers()
