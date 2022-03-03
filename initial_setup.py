import json

from requests import get, post
from os.path import join


class LCPStarter:
    def __init__(self, config):
        self.config = config
        self.lcp_config = self.get_lcp_self()

        print(self.config.lcp_parent_url)

        if self.lcp_config is None:
            self.set_lcp_config()
        else:
            self.tweak_lcp()

    def get_lcp_self(self):
        url = join(self.config.lcp_url, "self")

        headers = {
        }

        response = get(url, headers=headers)
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return json.loads(response.text)

        print(response)

    def set_lcp_config(self):
        headers = {
            "content-type": "application/json"
        }
        cfg = self.config.lcp_config
        cfg['type'] = 'LCPDescription'
        url = join(self.config.lcp_url, "self/configuration")

        response = post(url, json.dumps(cfg), headers=headers)

        assert(response.status_code == 201)

    def tweak_lcp(self):
        self.config.lcp_config['id'] = self.lcp_config['id']
        self.config.lcp_config['name'] = self.lcp_config['name']
        self.config.lcp_config['url'] = self.lcp_config['url']
        self.config.lcp_config['description'] = self.lcp_config['description']
