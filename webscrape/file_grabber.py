import requests
import bs4

base_url = "http://www.poetryfoundation.org/poem/"
# go to 300,000

for i in xrange(251287, 350000):
    url = base_url + str(i)
    response_object = requests.get(url)
    response_text = response_object.text
    if "no longer available" in response_text:
        print i
        continue
    elif "404 error" in response_text:
        print i
        continue
    else:
        soup = bs4.BeautifulSoup(response_text, "html.parser")
        print soup.title.string.strip()
        f = open(str(i) + ".text", "w")
        f.write(response_text.encode('utf8'))
        f.close()

print "COMPLETED THROUGH 300,000"
