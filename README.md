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
dade/Desktop/sephiroth via sephiroth
➜ python sephiroth.py --help
usage: Sephiroth [-h] -s {nginx} -c {aws} [-p] [--no-ipv6] [-V]

Sephiroth is made to help block clouds.

optional arguments:
  -h, --help            show this help message and exit
  -s {nginx}, --server {nginx}
                        Type of server to build blocklist for
  -c {aws}, --cloud {aws}
                        Cloud provider to block
  -p, --proxy           Using PROXY Protocol?
  --no-ipv6             Exclude ipv6 addresses from the block list where
                        applicable
  -V, --version         show program's version number and exit

For more information, assistance, or to submit a pull request, please visit
https://github.com/0xdade/sephiroth.
```

## Example

```
sephiroth on  master [!?] via sephiroth
➜ python sephiroth.py -s nginx -c aws -p
Your aws blocklist for nginx has been created: ./output/nginx_aws_2020-02-16_003003.conf
Please add this line to /etc/nginx/nginx.conf before the Virtual Host Configs.

        include /mnt/c/Users/dade/Desktop/sephiroth/output/nginx_aws_2020-02-16_003003.conf;

Then you can use the $block_ip variable in your site config like so:

        if ($block_ip) {
                return 302 https://example.com;
        }
```


## Supported Servers

* `nginx` - Makes use of nginx's "ngx_http_geo_module" which comes with the nginx package in Ubuntu 18.04. Optionally supports the use of `proxy_protocol`, in the event that you are using a PROXY-enabled redirector.

## Supported Cloud Providers

* Amazon Web Services - `aws`

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