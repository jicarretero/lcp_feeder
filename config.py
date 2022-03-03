import yaml


class Config:
    def __init__(self):
        with open("config.yml", "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        self.lcp_url = self.config['lcp_url']
        self.test_config_file = self.config['test_config_file']

        self.lcp_config = self.config['lcp_config']

        self.lcp_parent_url = self.config['lcp_parent_url'] if 'lcp_parent_url' in self.config else None
