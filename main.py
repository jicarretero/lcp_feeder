#!/usr/bin/env python3

from nmap_scanner import PortScanner
from config import Config
from models.SoftwareModel import SoftwareObjectsFromNmap
from requests import post
from initial_setup import LCPStarter

def set_self_software(config):

    ps = PortScanner(config)
    ps.read_tcp()
    ps.load_from_file_or_scan()

    print(SoftwareObjectsFromNmap.json())

    headers = {
        "content-type": "application/json",
        "Authorization": "GUARD eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNjE2NzgxMDU4IiwiZXhwIjoiMTY0ODMxNzA1OCIsIm5iZiI6MTYxNjc4MTA1OH0.4jC0t-VJwKR4e--LT-QU36hATUUbf530UL-fHj_bssE"
    }

    response = post(config.lcp_url + "/self/software", headers=headers, data=SoftwareObjectsFromNmap.json())

    print("Status Code: ", response.status_code)
    print(response.text)
    print(response.headers)


def initial_configuration(config):
    starter = LCPStarter(config)
    print(starter)


if __name__ == "__main__":
    config = Config()
    print(config.lcp_url)
    print(config.test_config_file)

    initial_configuration(config)

    # set_self_software(config)
