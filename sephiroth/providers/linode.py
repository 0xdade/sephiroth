from csv import DictReader
import io
import requests

from sephiroth.providers.base_provider import BaseProvider


class Linode(BaseProvider):
    def __init__(self):
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges()

    def _get_ranges(self):
        """
        Input: None
        Output: Dict representation of geoip.linode.com
        """
        print("(linode) Fetching Linode addresses from geoip.linode.com")
        fieldnames = ("prefix", "country", "subdivision", "city", "allocation_size")
        url = "https://geoip.linode.com/"
        r = requests.get(url)
        r.encoding = "utf-8"
        csvio = io.StringIO(r.text, newline="")
        return list(DictReader(csvio, fieldnames))

    def _process_ranges(self):
        """
        Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = ["(linode) Address nodes collected from geoip.linode.com"]
        out_ranges = []
        for address in self.source_ranges:
            if not address:
                continue
            if address["prefix"].startswith("# Last modified"):
                header_comments.append(f"(linode) {address['prefix'][2:]}")
                continue
            elif address["prefix"].startswith("#"):
                continue
            item = {
                "range": address["prefix"],
                "comment": f"{address['country']} {address['subdivision']} {address['city']}",
            }
            out_ranges.append(item)
        return {"header_comments": header_comments, "ranges": out_ranges}
