# Sephiroth

A Python3 script to build cloud block lists for servers.

## Requirements

* Python 3.8

## Setup


### Python
It is recommended to install sephiroth into a virtual environment. From a brand new Ubuntu 18.04 machine, the setup flow should look something like this:

```bash
sudo apt-get install python3 python3-pip && python -m pip install pipenv
mkdir sephiroth && cd sephiroth
pipenv install sephiroth
```

You can also get the always-latest updates by cloning directly from the repository.

```bash
git clone https://github.com/0xdade/sephiroth.git
cd sephiroth
pipenv install .
```

### Docker

Alternatively, we provide a [Dockerfile](/Dockerfile) with build and run instructions, or you can fetch the latest version from [dockerhub](https://hub.docker.com/r/0xdade/sephiroth):

```bash
docker pull 0xdade/sephiroth
docker run --rm -v $(pwd):/app/output sephiroth -s nginx -t gcp
```

## Usage

Sephiroth provides a built in help menu through the use of Python's argparse library. It tells you which commands are required, as well as other options.

```bash
sephiroth on  master [!] on 🐳 v19.03.12 via sephiroth via 🐍 3.8.3
➜ sephiroth --help
usage: Sephiroth [-h] -s {nginx,apache,iptables,ip6tables} -t {aws,azure,gcp,asn,file,oci,tor} [-a ASN] [-f FILENAME] [-r REDIR_TARGET] [-p] [--no-ipv6] [--compacted] [-V]

Sephiroth is made to help block clouds.

optional arguments:
  -h, --help            show this help message and exit
  -s {nginx,apache,iptables,ip6tables}, --server {nginx,apache,iptables,ip6tables}
                        Type of server to build blocklist for
  -t {aws,azure,gcp,asn,file,oci,tor}, --target {aws,azure,gcp,asn,file,oci,tor}
                        Targets to block
  -a ASN, --asn ASN     ASN to block in AS#### format
  -f FILENAME, --file FILENAME
                        Files to block addresses from
  -r REDIR_TARGET, --redir REDIR_TARGET
                        Place to redirect requests to. (apache)
  -p, --proxy           Using PROXY Protocol? (nginx)
  --no-ipv6             Exclude ipv6 addresses from the block list where applicable
  --compacted           Compact neighboring cidr ranges. This produces smaller file sizes but loses detail about each range.
  -V, --version         show program's version number and exit

For more information, assistance, or to submit a pull request, please visit https://github.com/0xdade/sephiroth.
```

## Example

```bash
sephiroth on  master [!?] on 🐳 v19.03.8 via sephiroth took 7s
➜ sephiroth -s nginx -t asn -a AS15169 -a AS31337 -t aws
(asn) Fetching IP ranges from api.hackertarget.com for 2 ASNs
(aws) Fetching IP ranges from Amazon
Your nginx blocklist for asn, aws can be found at output/2020-06-07_002847_nginx_asn_aws.conf

Please add this line to /etc/nginx/nginx.conf before the Virtual Host Configs.

        include /mnt/c/Users/dade/Desktop/sephiroth/output/2020-06-07_002847_nginx_asn_aws.conf;

Then you can use the $block_ip variable in your site config like so:

        if ($block_ip) {
                return 302 https://example.com;
        }

```


## Supported Servers

* `nginx` - Makes use of nginx's `ngx_http_geo_module` which comes with the nginx package in Ubuntu 18.04. Optionally supports the use of `proxy_protocol`, in the event that you are using a PROXY-enabled redirector.
* `apache` - Generates a mod_rewrite rule set to do conditional redirects based on cloud ip ranges. Does not (to my knowledge) support `proxy_protocol` usage. Requires `-r REDIR_TARGET` for the RewriteRule
* `iptables` - Generates a set of iptables DROP rules to block access from listed IPv4 ranges.
* `ip6tables` - Generates a set of ip6tables DROP rules to block access from listed IPv6 ranges.

## Supported Providers

While Sephiroth began as a cloud blocking script, it became apparent that there were plenty of other sources of ip addresses that might be useful, and so we expanded. This is the list of currently supported providers.

* `aws` - Amazon Web Services. Obtained via the [documented download process](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-download).
* `azure` - Azure Cloud. Fetched via a two part process. Fetch the html of [the download page](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519) and then parse the html to get the `failoverLink` anchor tag. That JSON is then downloaded.
* `gcp` - Google Cloud Platform. Fetches the `cloud.json` as documented via the [docs](https://cloud.google.com/compute/docs/faq#find_ip_range).
* `oci` - Oracle Cloud Infrastructure. Fetched via the [documented download process](https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/addressranges.htm)
* `asn` - Lookup IP ranges by ASN. Uses [Hackertarget](https://hackertarget.com/as-ip-lookup/) API to make fetching results painless. Limited to 100 ASN lookups per day per source IP.
* `file` - Read line-separated list of addresses from one or more files. Lines that begin with # are ignored and lines that contain a # after the address save the comment into the output.
* `tor` - Fetch the bulk list of Tor exit nodes from the torproject.org website and add them to the list.

## Acknowledgements

These are resources I found while building sephiroth that I thought were quite helpful

* [curi0usJack's](https://twitter.com/curi0usJack) [mod_rewrite rules gist](https://gist.github.com/curi0usJack/971385e8334e189d93a6cb4671238b10)
* [Enjen ASN Blocklist](https://www.enjen.net/asn-blocklist/readme.php) - [Example](https://www.enjen.net/asn-blocklist/index.php?asn=15169&type=nginx)

## License

```text
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
