# Sephiroth

A Python3 script to build cloud block lists for servers.

## Requirements

* Python 3.6+ (Sephiroth makes use of f-strings)

## Setup

It is recommended to install the requirements into a virtual environment. From a brand new Ubuntu 18.04 machine, the setup flow should look something like this:

```
$ sudo apt install python3 python3-venv git
$ git clone https://github.com/0xdade/sephiroth.git
$ cd sephiroth/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

Sephiroth provides a built in help menu through the use of Python's argparse library. It tells you which commands are required, as well as other options.

```
sephiroth on  master [!?] on 🐳 v19.03.8 via sephiroth
➜ ./sephiroth.py --help
usage: Sephiroth [-h] -s {nginx,apache} -c {aws,azure,gcp,oci} [-p]
                 [--no-ipv6] [-V]

Sephiroth is made to help block clouds.

optional arguments:
  -h, --help            show this help message and exit
  -s {nginx,apache}, --server {nginx,apache}
                        Type of server to build blocklist for
  -c {aws,azure,gcp,oci}, --cloud {aws,azure,gcp,oci}
                        Cloud provider(s) to block
  -p, --proxy           Using PROXY Protocol?
  --no-ipv6             Exclude ipv6 addresses from the block list where
                        applicable
  -V, --version         show program's version number and exit

For more information, assistance, or to submit a pull request, please visit
https://github.com/0xdade/sephiroth.
```

## Example

```
sephiroth on  master [!] via sephiroth took 6s
➜ python sephiroth.py -s nginx -c aws -c azure
Your nginx blocklist for aws, azure can be found at ./output/nginx_aws_azure_2020-02-16_040129.conf

Please add this line to /etc/nginx/nginx.conf before the Virtual Host Configs.

        include /mnt/c/Users/dade/Desktop/sephiroth/output/nginx_aws_azure_2020-02-16_040129.conf;

Then you can use the $block_ip variable in your site config like so:

        if ($block_ip) {
                return 302 https://example.com;
        }
```


## Supported Servers

* `nginx` - Makes use of nginx's "ngx_http_geo_module" which comes with the nginx package in Ubuntu 18.04. Optionally supports the use of `proxy_protocol`, in the event that you are using a PROXY-enabled redirector.
* `apache` - Generates a mod_rewrite rule set to do conditional redirects based on cloud ip ranges. Does not (to my knowledge) support `proxy_protocol` usage. Requires `-r REDIR_TARGET` for the RewriteRule

## Supported Cloud Providers

* `aws` - Amazon Web Services. Obtained via the [documented download process](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-download).
* `azure` - Azure Cloud. Fetched via a two part process. Fetch the html of [the download page](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519) and then parse the html to get the `failoverLink` anchor tag. That JSON is then downloaded.
* `gcp` - Google Cloud Platform. Fetched via the absolutely insane abuse of spf records as outlined in the [docs](https://cloud.google.com/compute/docs/faq#find_ip_range).
* (DISABLED) `oci` - Oracle Cloud Infrastructure. Fetched via the [documented download process](https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/addressranges.htm) - KNOWN BUG SEE [#11](https://github.com/0xdade/sephiroth/issues/11)

## Acknowledgements

* [curi0usJack's](https://twitter.com/curi0usJack) [mod_rewrite rules gist](https://gist.github.com/curi0usJack/971385e8334e189d93a6cb4671238b10)

## License

```
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