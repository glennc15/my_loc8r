

from urllib.parse import urlsplit, urlunsplit


class UrlBuilder(object):
	'''

	Takes a base url and adds path and query parameters as needed using urlparse.


	'''


	def __init__(self, url):
		'''
		

		'''


		self._scheme, self._netloc, path, query, fragment = urlsplit(url)





	def url(self, path_parts, query=None):
		'''
		
		path_parts can be a list for multiple paths
		Example: ['api', 'locations', '123']

		will build 'api/locaitons/123'
		
		path_parts can also be a single string.


		'''

		if isinstance(path_parts, str):
			path_parts = [path_parts]


		path = '/'.join(s.strip('/') for s in path_parts)
		url = urlunsplit((self._scheme, self._netloc, path, query, None))


		return url 