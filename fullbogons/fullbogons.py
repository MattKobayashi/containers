# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jinja2==3.1.6",
#     "requests==2.32.3",
# ]
# ///

#!/usr/bin/env python3

from ipaddress import ip_network
import os
import jinja2
import requests

options = {}

# Variables
options["bird_router_id"] = os.environ['BIRD_ROUTER_ID']
options["bird_asn"] = os.environ['BIRD_ASN']
options["bird_debug"] = os.environ['BIRD_DEBUG']

# Load jinja2 config
templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(
    loader=templateLoader,
    trim_blocks=True,
    lstrip_blocks=False,
    keep_trailing_newline=True
    )

# Download and process raw fullbogon lists
print("Downloading and processing raw fullbogon lists...")
fullbogons_ipv4_raw = requests.get(
    'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt'
).text
fullbogons_ipv6_raw = requests.get(
    'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt'
).text

# Import BIRD peers
options["bird_peers"] = {}
for peer in os.environ['BIRD_PEERS'].split(";"):
    try:
        if ip_network(peer.split(",")[1]):
            options["bird_peers"][peer.split(",")[0]] = peer.split(",")[1]
    except ValueError:
        print(
            peer.split(",")[1],
            'is not a valid IP address or prefix, skipping...'
        )
        continue

# Import excluded prefixes
excluded_prefixes = []
for prefix in os.environ['BIRD_EXCLUDED_PREFIXES'].split(";"):
    try:
        if ip_network(prefix):
            excluded_prefixes.append(prefix)
    except ValueError:
        print(prefix, 'is not a valid IP address or prefix, skipping...')
        continue

# Create list of IPv4 fullbogons
print("Creating IPv4 fullbogons list...")
options["fullbogons_ipv4"] = []
for line in fullbogons_ipv4_raw.split('\n'):
    try:
        REMOVE = False
        for excluded_prefix in excluded_prefixes:
            if ip_network(excluded_prefix).overlaps(ip_network(line)):
                REMOVE = True
        if REMOVE is True:
            print(line, "overlaps with an excluded IPv4 prefix, skipping...")
            continue
        else:
            options["fullbogons_ipv4"].append(str(ip_network(line)))
    except ValueError:
        print(line, 'is not a valid IPv4 subnet, skipping...')
        continue

# Create list of IPv6 fullbogons
print("Creating IPv6 fullbogons list...")
options["fullbogons_ipv6"] = []
for line in fullbogons_ipv6_raw.split('\n'):
    try:
        REMOVE = False
        for excluded_prefix in excluded_prefixes:
            if ip_network(excluded_prefix).overlaps(ip_network(line)):
                REMOVE = True
        if REMOVE is True:
            print(line, "overlaps with an excluded IPv6 prefix, skipping...")
            continue
        else:
            options["fullbogons_ipv6"].append(str(ip_network(line)))
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
birdconf_file = open(
    "./bird.conf",
    "w",
    encoding="utf-8"
)
birdconf_file.write(birdconf)
birdconf_file.close()

