import requests
from .base_provider import BaseProvider

class AWS(BaseProvider):

	def __init__(self, excludeip6=False):
		self.source_ranges = self._get_ranges()
		self.processed_ranges = self._process_ranges(excludeip6)
	
	def _get_ranges(self):
		'''
		Input: None
		Output: Dict representation of ip-ranges.json
		'''
		aws_ip_ranges_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
		r = requests.get(aws_ip_ranges_url)
		return r.json()

	def _process_ranges(self, excludeip6=False):
		''' 
		Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
		Output: Dict with header_comments and list of dicts for ip ranges 
		'''
		header_comments = [
			f"syncToken: {self.source_ranges['syncToken']}", 
			f"createDate: {self.source_ranges['createDate']}"
		]
		out_ranges = []
		source_prefixes = self.source_ranges['prefixes']
		if not excludeip6:
			source_prefixes += self.source_ranges['ipv6_prefixes']
		
		for prefix in source_prefixes:
			if 'ipv6_prefix' in prefix:
				item_prefix = prefix['ipv6_prefix']
				iptype = "ipv6"
			else:
				item_prefix = prefix['ip_prefix']
				iptype = "ipv4"
			item = {"range": item_prefix, "comment": f"{iptype} {prefix['region']} {prefix['service']}" }
			out_ranges.append(item)
		
		output = {"header_comments": header_comments, "ranges": out_ranges}
		return output