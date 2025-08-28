from netaddr import IPNetwork, IPSet

from sephiroth.providers.asn import ASN
from sephiroth.providers.aws import AWS
from sephiroth.providers.azure import Azure
from sephiroth.providers.cloudflare import Cloudflare
from sephiroth.providers.do import DO
from sephiroth.providers.file import File
from sephiroth.providers.remote_file import RemoteFile
from sephiroth.providers.gcp import GCP
from sephiroth.providers.linode import Linode
from sephiroth.providers.oci import OCI
from sephiroth.providers.tor import Tor
from sephiroth.providers.vultr import Vultr

classmap = {
    "aws": AWS,
    "azure": Azure,
    "gcp": GCP,
    "oci": OCI,
    "asn": ASN,
    "file": File,
    "remote-file": RemoteFile,
    "tor": Tor,
    "do": DO,
    "linode": Linode,
    "cloudflare": Cloudflare,
    "vultr": Vultr,
}

supported_targets = [*list(classmap.keys()), "_all"]


class Provider:
    def __init__(self, provider, targets_in=None):
        if targets_in:
            self.provider = classmap[provider](targets_in)
        else:
            self.provider = classmap[provider]()

    def get_processed_ranges(self):
        return self.provider.get_processed_ranges()

    def get_compacted_ranges(self):
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


__all__ = [
    "Provider",
]
