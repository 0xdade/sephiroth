#!/usr/bin/env python3
'''
This script makes use of f-strings, introduced in python 3.6.
'''

from datetime import datetime
import argparse
import os
from pathlib import Path

import requests
from jinja2 import Template

__author__ = "0xdade"
SEPHIROTH_VERSION = "1.0"
supported_servers = [
	"nginx"
]

supported_clouds = [
	"aws"
]

base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, 'output')
template_dir = os.path.join(base_dir, 'templates')
help_templates_dir = os.path.join(template_dir, 'help')


def get_output_path(servertype, provider, build_date):
	'''
	Input: Server type, date from build_template(), cloud provider
	Output: Path to file on disk to write to
	'''
	fdate = build_date.strftime('%Y-%m-%d_%H%M%S')
	fname = f"{servertype}_{provider}_{fdate}.conf"
	return os.path.join(output_dir, fname)


def download_aws_ranges():
	'''
	Input: None
	Output: Dict representation of ip-ranges.json
	'''
	aws_ip_ranges_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
	r = requests.get(aws_ip_ranges_url)
	return r.json()

def process_aws_ranges(ranges, excludeip6=False):
	''' 
	Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
	Output: Dict with header_comments and list of dicts for ip ranges 
	'''
	header_comments = [
		f"syncToken: {ranges['syncToken']}", 
		f"createDate: {ranges['createDate']}"
	]
	out_ranges = []
	source_prefixes = ranges['prefixes']
	if not excludeip6:
		source_prefixes += ranges['ipv6_prefixes']
	
	for prefix in source_prefixes:
		if 'ipv6_prefix' in prefix:
			item_prefix = prefix['ipv6_prefix']
			iptype = "ipv6"
		else:
			item_prefix = prefix['ip_prefix']
			iptype = "ipv4"
		item = {"range": item_prefix, "comment": f"{iptype} {prefix['region']} {prefix['service']}" }
		out_ranges.append(item)
	
	output = {"header_comments": header_comments, "ranges": out_ranges}
	return output

def get_ranges(provider, excludeip6):
	if provider == 'aws':
		awsranges = download_aws_ranges()
		template_vars = process_aws_ranges(awsranges, excludeip6)

	return template_vars

def get_template(servertype):
	'''
	Input: String name of server type
	Output: Jinja2 template object for given server type
	'''
	fname = f"{servertype}.jinja"
	template_path = os.path.join(template_dir, fname)
	template = Template(open(template_path).read())
	return template

def build_template(ranges, template, build_date, use_proxy=False):
	'''
	Input: output of process_<provider>_ranges(), output of get_template()
	Output: Rendered template string ready to write to disk
	'''
	template_output = template.render(
		ranges=ranges['ranges'],
		header_comments=ranges['header_comments'],
		build_date=build_date,
		use_proxy=use_proxy
	)
	return template_output

def print_output(servertype, provider, outfile):
	helpfile = os.path.join(help_templates_dir, servertype) + '.jinja'
	abspath = os.path.abspath(outfile)
	help_text = Template(open(helpfile).read()).render(provider=provider, servertype=servertype, outfile=outfile, abspath=abspath)
	print(f"Your {provider} blocklist for {servertype} can be found at ./{outfile}\n")
	print(help_text)

def parse_args():
	parser_desc = "Sephiroth is made to help block clouds."
	parser_epilog = "For more information, assistance, or to submit a pull request, please visit https://github.com/0xdade/sephiroth."
	parser = argparse.ArgumentParser(prog="Sephiroth", description=parser_desc, epilog=parser_epilog)
	parser.add_argument(
		"-s", 
		"--server", 
		help="Type of server to build blocklist for", 
		required=True, 
		choices=supported_servers,
		dest='servertype'
	)
	parser.add_argument(
		"-c", 
		"--cloud", 
		help="Cloud provider to block",
		required=True,
		choices=supported_clouds,
		dest='provider'
	)
	parser.add_argument(
		"-p", 
		"--proxy", 
		help="Using PROXY Protocol?",
		default=False,
		action='store_true',
		dest='use_proxy'
	)
	parser.add_argument( 
		"--no-ipv6", 
		help="Exclude ipv6 addresses from the block list where applicable",
		default=False,
		action='store_true',
		dest='excludeip6'
	)
	parser.add_argument(
		"-V",
		"--version",
		action="version",
		version="%(prog)s " + SEPHIROTH_VERSION
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_args()
	build_date = datetime.utcnow()
	template_vars = get_ranges(args.provider, args.excludeip6)
	template = get_template(args.servertype)
	template_output = build_template(template_vars, template, build_date, args.use_proxy)
	outfile = get_output_path(args.servertype, args.provider, build_date)
	if not Path(output_dir).exists():
		Path(output_dir).mkdir()
	with open(outfile, 'w') as o:
		o.write(template_output)
	
	print_output(args.servertype, args.provider, outfile)

if __name__ == "__main__":
	main()