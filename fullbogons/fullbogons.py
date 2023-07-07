#!/usr/bin/env python3

import requests
import ipaddress
import jinja2
import os

options = {}

# Variables
fullbogons_ipv4_url = 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt'
fullbogons_ipv6_url = 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt'
options["bird_router_id"] = os.environ['BIRD_ROUTER_ID']
options["bird_asn"] = os.environ['BIRD_ASN']

# Load jinja2 config
templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(
    loader=templateLoader,
    trim_blocks=True,
    lstrip_blocks=False,
    keep_trailing_newline=True
    )

# Do stuff
fullbogons_ipv4_raw = requests.get(fullbogons_ipv4_url).text
fullbogons_ipv6_raw = requests.get(fullbogons_ipv6_url).text
options["bird_peers"] = {}
for peer in os.environ['BIRD_PEERS'].split(";"):
    options["bird_peers"][peer.split(",")[0]] = peer.split(",")[1]

# Create list of IPv4 fullbogons
print("Creating IPv4 fullbogons list...")
options["fullbogons_ipv4"] = []
for line in fullbogons_ipv4_raw.split('\n'):
    try:
        options["fullbogons_ipv4"].append(str(ipaddress.ip_network(line)))
    except ValueError:
        print(line, 'is not a valid IPv4 subnet, skipping...')
        continue

# Create list of IPv6 fullbogons
print("Creating IPv6 fullbogons list...")
options["fullbogons_ipv6"] = []
for line in fullbogons_ipv6_raw.split('\n'):
    try:
        options["fullbogons_ipv6"].append(str(ipaddress.ip_network(line)))
    except ValueError:
        print(line, 'is not a valid IPv6 subnet, skipping...')
        continue

# Generate BIRD config
print("Generating BIRD configuration...")
TEMPLATE_FILE = "bird.j2"
template = templateEnv.get_template(TEMPLATE_FILE)
birdconf = template.render(options)

# Save BIRD config to file
print("Saving BIRD configuration to bird.conf...")
birdconf_file = open("./bird.conf", "w")
birdconf_file.write(birdconf)
birdconf_file.close()
