import requests
from sephiroth.providers.base_provider import BaseProvider


class GCP(BaseProvider):
    def __init__(self, excludeip6=False):
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges(excludeip6)

    def _get_ranges(self):
        """
        Input: None
        Output: Dict representation of cloud.json
        """
        print("(gcp) Fetching IP ranges from Google")
        gcp_ip_ranges_url = "https://www.gstatic.com/ipranges/cloud.json"
        r = requests.get(gcp_ip_ranges_url)
        return r.json()

    def _process_ranges(self, excludeip6=False):
        """
        Input: Dict of cloud.json, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = [
            f"(gcp) syncToken: {self.source_ranges['syncToken']}",
            f"(gcp) creationTime: {self.source_ranges['creationTime']}",
        ]
        out_ranges = []
        source_prefixes = self.source_ranges["prefixes"]

        for prefix in source_prefixes:
            if "ipv4Prefix" in prefix:
                item_prefix = prefix["ipv4Prefix"]
                iptype = "ipv4"
            elif "ipv6Prefix" in prefix and not excludeip6:
                item_prefix = prefix["ipv6Prefix"]
                iptype = "ipv6"

            item = {
                "range": item_prefix,
                "comment": f"{iptype} {prefix['scope']} {prefix['service']}",
            }
            out_ranges.append(item)

        return {"header_comments": header_comments, "ranges": out_ranges}
