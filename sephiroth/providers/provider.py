from sephiroth.providers import AWS, Azure, GCP, OCI, ASN, File, Tor, DO

classmap = {
    "aws": AWS,
    "azure": Azure,
    "gcp": GCP,
    "oci": OCI,
    "asn": ASN,
    "file": File,
    "tor": Tor,
    "do": DO,
}


class Provider:
    def __init__(self, provider, targets_in=None):
        if targets_in:
            self.provider = classmap[provider](targets_in)
        else:
            self.provider = classmap[provider]()

    def get_processed_ranges(self):
        return self.provider.get_processed_ranges()

    def get_compacted_ranges(self):
        from netaddr import IPNetwork, IPSet

        processed = self.provider.get_processed_ranges()
        networks = [IPNetwork(cidr["range"]) for cidr in processed["ranges"]]
        compacted = [
            {
                "range": str(cidr),
                "comment": f"{type(self.provider).__name__.lower()} (compacted)",
            }
            for cidr in IPSet(networks).iter_cidrs()
        ]

        return {"header_comments": processed["header_comments"], "ranges": compacted}
