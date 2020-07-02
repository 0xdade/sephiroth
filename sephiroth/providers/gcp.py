import dns.resolver

from sephiroth.providers.base_provider import BaseProvider

"""
I know this probably looks ridiculous. But it's literally what they expect people to do.
https://cloud.google.com/compute/docs/faq#find_ip_range
"""


class GCP(BaseProvider):
    def __init__(self, excludeip6=False):
        self.seen_netblocks = set()
        self.seen_txt_records = set()
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges(excludeip6)

    def _parse_txt(self, txt):
        record = {"includes": [], "ip_ranges": []}
        for entry in txt.split(" "):
            if entry.startswith("include") and ":" in entry:
                record["includes"].append(entry.split(":")[1])
            elif entry.startswith("ip4") and ":" in entry:
                record["ip_ranges"].append(entry.split(":")[1])
        return record

    def _get_netblocks(self, query):
        if query in self.seen_txt_records:
            return
        answer = dns.resolver.query(query, "TXT")
        answers = [txt.to_text() for txt in answer]
        for txt in answers:
            record = self._parse_txt(txt)
        for include in record["includes"]:
            self._get_netblocks(include)
        for ip_range in record["ip_ranges"]:
            if ip_range not in self.seen_netblocks:
                self.seen_netblocks.add(ip_range)
        self.seen_txt_records.add(query)

    def _get_ranges(self):
        print("(gcp) Fetching IP ranges from Google")
        base_txt_record = "_cloud-netblocks.googleusercontent.com"
        self._get_netblocks(base_txt_record)
        return self.seen_netblocks

    def _process_ranges(self, excludeip6=False):
        header_comments = [
            f"(gcp) _cloud-netblocks count: {len(self.seen_txt_records)}"
        ]
        out_ranges = []
        for item in self.source_ranges:
            out_item = {"range": item, "comment": "ipv4 gcp ComputeEngine"}
            out_ranges.append(out_item)

        output = {"header_comments": header_comments, "ranges": out_ranges}
        return output
