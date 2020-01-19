import requests
import pprint

URL = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet'
page = requests.get(URL)

pprinter = pprint.PrettyPrinter()

# pprinter.pprint(page.content)

# found = page.content.find('Alberta Total Net Generation')

print(type(page.content))
