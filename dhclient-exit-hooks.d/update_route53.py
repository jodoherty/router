#!/usr/bin/python3

import boto3
import ipaddress
import json
import os
import os.path

def read_config(interface: str):
    config_file_path = os.getenv("CONFIG_FILE", "/etc/route53_dyndns.json")
    if not os.path.exists(config_file_path):
        return None
    with open(config_file_path, "rb") as f:
        all_config = json.load(f)
    if interface not in all_config:
        return None
    return all_config[interface]

def get_client(config):
    client = boto3.client("route53", **config["client_options"])
    return client

def update_a_records(interface: str, address: ipaddress.IPv4Address)-> None:
    address_value = address.compressed
    config = read_config(interface)
    if not config:
        print(f"no configuration for {interface}")
        return
    client = get_client(config)
    for zone_id in config["zones"]:
        for hostname in config["zones"][zone_id]:
            changes = [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': hostname,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': address_value}],
                    },
                },
            ]
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={'Changes': changes})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise(RuntimeError('Update failed {}'.format(json.dumps(response))))

def update_aaaa_records(interface: str, address: ipaddress.IPv6Address) -> None:
    address_value = address.compressed
    config = read_config(interface)
    if not config:
        print(f"no configuration for {interface}")
        return
    client = get_client(config)
    for zone_id in config["zones"]:
        for hostname in config["zones"][zone_id]:
            changes = [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': hostname,
                        'Type': 'AAAA',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': address_value}],
                    },
                },
            ]
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={'Changes': changes})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise(RuntimeError('Update failed {}'.format(json.dumps(response))))


if __name__ == "__main__":
    status = int(os.getenv("status", "0"))
    reason = os.getenv("reason")
    interface = os.getenv("interface")

    if interface and reason in ("BOUND", "RENEW", "REBIND", "REBOOT"):
        new_ip_address_value = os.getenv("new_ip_address")
        new_ip_address = None
        if new_ip_address_value:
            new_ip_address = ipaddress.IPv4Address(new_ip_address_value)
        if new_ip_address and new_ip_address.is_global:
            print(f"updating DNS A records")
            update_a_records(interface, new_ip_address)
    elif interface and reason in ("BOUND6", "RENEW6", "REBIND6"):
        new_ip6_address_value = os.getenv("new_ip6_address")
        new_ip6_prefixlen_value = os.getenv("new_ip6_prefixlen")
        new_ip6_prefix_value = os.getenv("new_ip6_prefix")
        ip6_address = None
        if new_ip6_address_value and new_ip6_prefixlen_value:
            ip6_address = ipaddress.IPv6Address(new_ip6_address_value + "/" + new_ip6_prefixlen_value)
        elif new_ip6_prefix_value:
            ip6_address = ipaddress.IPv6Network(new_ip6_prefix_value)[1]
        if ip6_address and ip6_address.is_global:
            print("updating DNS AAAA records")
            update_aaaa_records(interface, ip6_address)
