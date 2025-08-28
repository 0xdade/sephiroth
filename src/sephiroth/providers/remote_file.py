import requests
from sephiroth.providers.base_provider import BaseProvider

class RemoteFile(BaseProvider):
    def __init__(self, urls: list[str], excludeip6: bool = False):
        self.urls = urls
        self.excludeip6 = excludeip6
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges()

    def _get_ranges(self) -> dict:
        ranges = {}
        for url in self.urls:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                lines = resp.text.splitlines()
                ranges[url] = [line + "\n" for line in lines]
            except Exception as e:
                print(f"[!] Failed to fetch {url}: {e}")
        return ranges

    def _process_ranges(self) -> dict:
        ranges = []
        for fname, range_list in self.source_ranges.items():
            for ip_line in range_list:
                if ip_line.startswith("#"):
                    continue
                if ":" in ip_line and self.excludeip6:
                    continue
                if "#" in ip_line:
                    ip_addr, comment = map(str.strip, ip_line.split("#", 1))
                else:
                    ip_addr = ip_line.strip()
                    comment = ""
                ranges.append({
                    "range": ip_addr,
                    "comment": f"{fname} {comment}".strip()
                })

        return {
            "header_comments": [f"(remote-file) Fetched from {', '.join(self.urls)}"],
            "ranges": ranges
        }

