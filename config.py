import yaml


class Config:
    def __init__(self):
        with open("config.yml", "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        self.lcp_url = self.config['lcp_url']
        self.test_config_file = self.config['test_config_file']

        self.lcp_config = self.config['lcp_config']

        self.lcp_parent_url = self.config['lcp_parent_url'] if 'lcp_parent_url' in self.config else None

        self.skip_local_scanning = self.config['skip_local_scanning'] if 'skip_local_scanning' in self.config else {}
        if 'udp_ports' not in self.skip_local_scanning:
            self.skip_local_scanning['udp_ports'] = []
        if 'tcp_ports' not in self.skip_local_scanning:
            self.skip_local_scanning['tcp_ports'] = []

        self.headers = self.config['headers'] if 'headers' in self.config else {}

    def get_headers(self, default_headers={}):
        h = self.headers.copy()
        h.update(default_headers)
        return h
