import urllib2

url = 'http://www.cnbeta.com'
request = urllib2.Request(url)
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1601.1 Safari/537.36')
reader = urllib2.urlopen(request)
print reader.read()
