import CloudFlare
import operator
import requests

from collections import defaultdict
from pprint import pprint

import os

"""
Use CF_API_EMAIL and CF_API_KEY env vars
"""

def main():
    my_ip = requests.get('https://api.ipify.org').text
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    zone_id = zones[0]['id']
    zone_name = zones[0]['name']
    dns_records = cf.zones.dns_records.get(zone_id, params={'per_page': 100})
    a_records = list(filter(lambda zone: zone['type'] == 'A', dns_records))
    txt_records = list(filter(lambda zone: zone['type'] == 'TXT', dns_records))
    a_domains = [record['name'] for record in a_records]

    # dns_prefix is needed within external-dns because without it, A records with the LAN IP are automatically deleted
    dns_prefix = os.getenv("CF_DNS_PREFIX")
    assert dns_prefix, "CF_DNS_PREFIX must be set"

    print(a_domains)
    txt_domains_to_create = []
    for txt_record in txt_records:
        if "heritage=external-dns" in txt_record['content'] and txt_record['name'].replace(dns_prefix, '', 1) not in a_domains:
            txt_domains_to_create.append(txt_record['name'])

    for domain in txt_domains_to_create:
        if domain in a_domains:
            continue
        dns_record  = { 'name': domain.replace('.' + zone_name, '').replace(dns_prefix, '', 1), 'type':'A', 'content': my_ip, 'proxied': True }
        cf.zones.dns_records.post(zone_id, data=dns_record)
        print(f'Created A record for {domain}')

if __name__ == "__main__":
    main()
    print("done")
