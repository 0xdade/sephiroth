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

from providers import Provider

__author__ = "0xdade"
SEPHIROTH_VERSION = "1.0"
supported_servers = [
	"nginx"
]

supported_clouds = [
	"aws",
	"azure"
]

base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, 'output')
template_dir = os.path.join(base_dir, 'templates')


def get_output_path(servertype, providers, build_date):
	'''
	Input: Server type, date from build_template(), cloud provider
	Output: Path to file on disk to write to
	'''
	providers_str = '_'.join(providers)
	fdate = build_date.strftime('%Y-%m-%d_%H%M%S')
	fname = f"{servertype}_{providers_str}_{fdate}.conf"
	return os.path.join(output_dir, fname)


def get_ranges(selected_provider, excludeip6):
	provider = Provider(selected_provider)
	template_vars = provider.get_processed_ranges()

	return template_vars

def get_template(servertype):
	'''
	Input: String name of server type
	Output: Jinja2 template object for given server type
	'''
	fname = f"{servertype}/conf.jinja"
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

def print_output(servertype, providers, outfile):
	helpfile = os.path.join(template_dir, servertype, 'help.jinja')
	abspath = os.path.abspath(outfile)
	providers_str = ', '.join(providers)
	help_text = Template(open(helpfile).read()).render(abspath=abspath)
	print(f"Your {servertype} blocklist for {providers_str} can be found at ./{outfile}\n")
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
		action='append',
		dest='providers'
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
	template_vars = {"header_comments": [], "ranges": []}
	for provider in args.providers:
		provider_vars = get_ranges(provider, args.excludeip6)
		template_vars['header_comments'] += provider_vars['header_comments']
		template_vars['ranges'] += provider_vars['ranges']
	template = get_template(args.servertype)
	template_output = build_template(template_vars, template, build_date, args.use_proxy)
	outfile = get_output_path(args.servertype, args.providers, build_date)
	if not Path(output_dir).exists():
		Path(output_dir).mkdir()
	with open(outfile, 'w') as o:
		o.write(template_output)
	
	print_output(args.servertype, args.providers, outfile)

if __name__ == "__main__":
	main()