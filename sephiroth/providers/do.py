import requests
import io
from csv import DictReader

from sephiroth.providers.base_provider import BaseProvider


class DO(BaseProvider):
    def __init__(self, excludeip6=False):
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges(excludeip6)

    def _get_ranges(self):
        """
        Input: None
        Output: Dict representation of google.csv from DO
        """
        print("(do) Fetching IP ranges from Digital Ocean")

        # The URL for this CSV is published on the DO Platform page:
        # https://www.digitalocean.com/docs/platform/
        # They indicate it is updated automatically, but they don't publish a
        # definition of the headers or policy regarding its' update or use.
        do_ip_ranges_url = "https://digitalocean.com/geo/google.csv"
        fieldnames = ("prefix", "country", "region", "city", "postalcode")

        r = requests.get(do_ip_ranges_url)
        r.encoding = "utf-8"
        csvio = io.StringIO(r.text, newline="")
        return list(DictReader(csvio, fieldnames))

    def _process_ranges(self, excludeip6=False):
        """
        Input: Dict of google.csv, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = [
            "(do) IP ranges collected from https://digitalocean.com/geo/google.csv"
        ]

        out_ranges = []
        source_prefixes = self.source_ranges

        for prefix in source_prefixes:
            if ":" in prefix["prefix"]:
                iptype = "ipv6"
                if excludeip6:
                    continue
            else:
                iptype = "ipv4"

            item_prefix = prefix["prefix"]

            item = {
                "range": item_prefix,
                "comment": f"{iptype} {prefix['region']} {prefix['city']}",
            }
            out_ranges.append(item)

        return {"header_comments": header_comments, "ranges": out_ranges}
