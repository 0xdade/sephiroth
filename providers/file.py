import requests
import os
from .base_provider import BaseProvider

class File(BaseProvider):

	def __init__(self,  targets_in, excludeip6=False):
		self.source_ranges = self._get_ranges(targets_in)
		self.processed_ranges = self._process_ranges(excludeip6)

	def _get_ranges(self, target_files):
		'''
		Input: List of filenames to read from
		Output: Dict representation of ip-ranges.json
		'''
		ranges = {}
		print(f"(file) Reading IP ranges from {len(target_files)} files")
		for infile in target_files:
			with open(infile, 'r') as f:
				ranges[os.path.basename(infile)] = f.readlines()
		return ranges


	def _process_ranges(self, excludeip6=False):
		''' 
		Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
		Output: Dict with header_comments and list of dicts for ip ranges 
		'''
		header_comments = [
			f"(file) Ranges provided from {len(self.source_ranges.items())} input files"
		]
		out_ranges = []
		for fname,range_list in self.source_ranges.items():
			for ip_line in range_list:
				if ip_line.startswith('#'):
					continue
				if ':' in ip_line and excludeip6:
					continue
				if '#' in ip_line:
					ip_addr = ip_line.split('#')[0].strip()
					comment = ip_line.split('#')[1].strip()
				else:
					ip_addr = ip_line.strip()
					comment = ''

				item = {"range": ip_addr, "comment": f"{fname} {comment}"}
				out_ranges.append(item)
		output = {"header_comments": header_comments, "ranges": out_ranges}
		return output