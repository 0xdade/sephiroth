import requests
from sephiroth.providers.base_provider import BaseProvider


class Cloudflare(BaseProvider):
    def __init__(self, excludeip6=False):
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges(excludeip6)

    def _get_ranges(self):
        """
        Input: None
        Output: Dict representation of cloudflare ip ranges
        """
        print("(cloudflare) Fetching IP ranges from cloudflare's API")
        cloudflare_ip_ranges_url = "https://api.cloudflare.com/client/v4/ips"
        r = requests.get(cloudflare_ip_ranges_url)
        return r.json()

    def _process_ranges(self, excludeip6=False):
        """
        Input: List of ip-ranges, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = [
            f"(cloudflare) success: {self.source_ranges['success']}",
            f"(cloudflare) messages: {self.source_ranges['messages']}",
        ]
        out_ranges = []
        ip_ranges = self.source_ranges["result"]

        range_types = [("ipv4_cidrs", "ipv4 cloudflare")]

        if not excludeip6:
            range_types.append(("ipv6_cidrs", "ipv6 cloudflare"))

        for range_type, comment in range_types:
            for ip_range in ip_ranges[range_type]:
                item = {
                    "range": ip_range,
                    "comment": comment
                }
                out_ranges.append(item)

        return {"header_comments": header_comments, "ranges": out_ranges}
