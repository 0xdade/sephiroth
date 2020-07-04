import requests
from sephiroth.providers.base_provider import BaseProvider


class ASN(BaseProvider):
    def __init__(self, targets_in, excludeip6=False):
        self.source_ranges = self._get_ranges(targets_in)
        self.processed_ranges = self._process_ranges(excludeip6)

    def _get_ranges(self, asns):
        """
        Input: List of ASNs in AS#### format
        Output: Dict representation of ip-ranges.json
        """
        ranges = {}
        print(
            f"(asn) Fetching IP ranges from api.hackertarget.com for {len(asns)} ASNs"
        )
        for a in asns:
            asn_lookup_url = f"https://api.hackertarget.com/aslookup/?q={a}"
            r = requests.get(asn_lookup_url)
            # the first result from this API is always the ASN name and number
            ranges[a] = r.content.decode("utf-8").split("\n")[1:]
        return ranges

    def _process_ranges(self, excludeip6=False):
        """
        Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = ["(asn) ASN Data collected from api.hackertarget.com"]
        out_ranges = []
        for asn, range_list in self.source_ranges.items():
            for ip_range in range_list:
                if ":" in ip_range and excludeip6:
                    continue
                item = {"range": ip_range, "comment": f"{asn}"}
                out_ranges.append(item)
        return {"header_comments": header_comments, "ranges": out_ranges}
