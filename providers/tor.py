import requests
from .base_provider import BaseProvider

class Tor(BaseProvider):

	def __init__(self, excludeip6=False):
		self.source_ranges = self._get_ranges()
		self.processed_ranges = self._process_ranges()

	def _get_ranges(self):
		'''
		Input: None
		Output: List of ip addresses
		'''
		print(f"(tor) Fetching Tor exit nodes from torproject.org")
		exit_list_url = 'https://check.torproject.org/torbulkexitlist'
		r = requests.get(exit_list_url)
		return r.content.decode('utf-8').split('\n')

	def _process_ranges(self):
		''' 
		Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
		Output: Dict with header_comments and list of dicts for ip ranges 
		'''
		header_comments = [
			f"(tor) Exit nodes collected from from check.torproject.org"
		]
		out_ranges = []
		for address in self.source_ranges:
			item = {"range": address, "comment": f"tor exit node"}
			out_ranges.append(item)
		output = {"header_comments": header_comments, "ranges": out_ranges}
		return output
