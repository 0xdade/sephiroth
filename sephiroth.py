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
	"nginx",
	'apache',
	'iptables',
	'ip6tables'
]

supported_targets = [
	"aws",
	"azure",
	"gcp",
	"asn",
	'file'
	#"oci"
]

base_dir = os.path.dirname(__file__)
output_dir = os.path.join(base_dir, 'output')
template_dir = os.path.join(base_dir, 'templates')

def get_output_path(servertype, targets, build_date):
	'''
	Input: Server type, date from build_template(), cloud provider
	Output: Path to file on disk to write to
	'''
	targets_str = '_'.join(targets)
	fdate = build_date.strftime('%Y-%m-%d_%H%M%S')
	fname = f"{fdate}_{servertype}_{targets_str}.conf"
	return os.path.join(output_dir, fname)


def get_ranges(selected_provider, excludeip6=False, targets_in=None):
	'''
	Input: Type of provider to target, as defined in supported_targets. 
		   Optionally exclude ip6, provide list of asns or files if asn or file target
	Output: Structured data ready to go to templates
	'''
	if targets_in:
		provider = Provider(selected_provider, targets_in)
	else:
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

def build_template(ranges, template, build_date, use_proxy=False, redir_target=''):
	'''
	Input: output of process_<provider>_ranges(), output of get_template()
	Output: Rendered template string ready to write to disk
	'''
	template_output = template.render(
		ranges=ranges['ranges'],
		header_comments=ranges['header_comments'],
		build_date=build_date,
		use_proxy=use_proxy,
		redir_target=redir_target
	)
	return template_output

def print_output(servertype, targets, outfile):
	helpfile = os.path.join(template_dir, servertype, 'help.jinja')
	abspath = os.path.abspath(outfile)
	targets_str = ', '.join(targets)
	help_text = Template(open(helpfile).read()).render(abspath=abspath, outfile=os.path.basename(outfile))
	print(f"Your {servertype} blocklist for {targets_str} can be found at {outfile}\n")
	print(help_text)

def validate_nginx_args(args):
	if args.redir_target:
		print("[?] Warning: We cannot generate nginx configs with redirect targets at this time. Ignoring.")
	return True

def validate_apache_args(args):
	if args.use_proxy:
		print("[?] Warning: We cannot use PROXY protocol with Apache at this time. Ignoring.")
	if args.redir_target is None:
		print("[!] Error: Apache requires a defined redirect target using -r")
		raise SystemExit
	elif args.redir_target.startswith('http://') or args.redir_target.startswith('https://'):
		print("[!] Error: Redirect target should not include scheme. Please edit the output RewriteRule directly if you want to change this.")
		raise SystemExit
	return True

def validate_iptables_args(args):
	print("[?] Warning: iptables rules automatically exclude any IPv6 addresses")
	return True

def validate_ip6tables_args(args):
	print("[?] Warning: ip6tables rules automatically exclude any IPv4 addresses")
	return True

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
		"-t", 
		"--target", 
		help="Targets to block",
		required=True,
		choices=supported_targets,
		action='append',
		dest='targets'
	)
	parser.add_argument(
		"-a",
		"--asn",
		help="ASN to block in AS#### format",
		action='append',
		metavar='ASN',
		dest="asns"
	)
	parser.add_argument(
		"-f",
		"--file",
		help="Files to block addresses from",
		action='append',
		metavar='FILENAME',
		dest="files"
	)
	parser.add_argument(
		"-r", 
		"--redir", 
		help="Place to redirect requests to. (apache)",
		default=None,
		dest='redir_target'
	)
	parser.add_argument(
		"-p", 
		"--proxy", 
		help="Using PROXY Protocol? (nginx)",
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

def validate_targets(args):
	success = True
	for target in args.targets:
		if target == 'asn' and not args.asns:
			print("[!] Error: Cannot specify -t asn without including at least one -a AS####")
			success = False
		elif target == 'file' and not args.files:
			print("[!] Error: Cannot specify -t file without including at least one -f filename.txt")
			success = False
	return success

server_validators = {
	'apache': validate_apache_args,
	'nginx': validate_nginx_args,
	'iptables': validate_iptables_args,
	'ip6tables': validate_ip6tables_args
}

def main():
	args = parse_args()
	if not validate_targets(args):
		raise SystemExit
	if args.servertype in server_validators:
		server_validators[args.servertype](args)
	build_date = datetime.utcnow()
	template_vars = {"header_comments": [], "ranges": []}
	for provider in args.targets:
		if args.asns and provider == 'asn':
			provider_vars = get_ranges(provider, excludeip6=args.excludeip6, targets_in=args.asns)
		elif args.files and provider == 'file':
			provider_vars = get_ranges(provider, excludeip6=args.excludeip6, targets_in=args.files)
		else:
			provider_vars = get_ranges(provider, excludeip6=args.excludeip6)
		template_vars['header_comments'] += provider_vars['header_comments']
		template_vars['ranges'] += provider_vars['ranges']
	template = get_template(args.servertype)
	template_output = build_template(template_vars, template, build_date, args.use_proxy, args.redir_target)
	outfile = get_output_path(args.servertype, args.targets, build_date)
	if not Path(output_dir).exists():
		Path(output_dir).mkdir()
	with open(outfile, 'w') as o:
		o.write(template_output)
	
	print_output(args.servertype, args.targets, outfile)

if __name__ == "__main__":
	main()