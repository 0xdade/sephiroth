import requests
from .base_provider import BaseProvider

class OCI(BaseProvider):

	def __init__(self, excludeip6=False):
		self.source_ranges = self._get_ranges()
		self.processed_ranges = self._process_ranges(excludeip6)
	
	def _get_ranges(self):
		'''
		Input: None
		Output: Dict representation of ip-ranges.json
		'''
		aws_ip_ranges_url = "https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json"
		r = requests.get(aws_ip_ranges_url)
		return r.json()

	def _process_ranges(self, excludeip6=False):
		''' 
		Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
		Output: Dict with header_comments and list of dicts for ip ranges 
		'''
		header_comments = [
			f"(oci) last_updated_timestamp: {self.source_ranges['last_updated_timestamp']}"
		]
		out_ranges = []
		
		for r in self.source_ranges['regions']:
			region = r["region"]
			for cidr in r["cidrs"]:
				item = {"range": cidr["cidr"], "comment": f"{region} {' '.join(cidr['tags'])}" }
				out_ranges.append(item)
		
		output = {"header_comments": header_comments, "ranges": out_ranges}
		return output