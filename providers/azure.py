import requests
from bs4 import BeautifulSoup

from .base_provider import BaseProvider

class Azure(BaseProvider):
	
	def __init__(self, excludeip6=False):
		self.source_ranges = self._get_ranges()
		self.processed_ranges = self._process_ranges(excludeip6)

	def _get_ranges(self):
		print(f"(azure) Fetching IP ranges from Microsoft")
		azure_download_page = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
		r = requests.get(azure_download_page)
		soup = BeautifulSoup(r.content, 'html.parser')
		direct_link = soup.select_one('.failoverLink')['href']
		r = requests.get(direct_link)
		return r.json()

	def _process_ranges(self, excludeip6=False):
		header_comments = [
			f"(azure) changeNumber: {self.source_ranges['changeNumber']}", 
			f"(azure) cloud: {self.source_ranges['cloud']}"
		]
		out_ranges = []
		for item in self.source_ranges['values']:
			name = item['name']
			platform = item['properties']['platform']
			for addr in item['properties']['addressPrefixes']:
				out_item = {"range": addr, "comment": f"{platform} {name}"}
				out_ranges.append(out_item)

		output = {"header_comments": header_comments, "ranges": out_ranges}
		return output

		