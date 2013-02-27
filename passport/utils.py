import re

def get_domain_from_url(url):
	"""
	get domain from a url string,
	for example:
		url="http://www.google.com/search"
		return "http://www.google.com"
	"""
	regex=re.compile(r'^(http:\/\/)?([^\/]+)')
	return regex.search(url).group(0)