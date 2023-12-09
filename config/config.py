from configparser import ConfigParser
import os
class Configuration():
    def __init__(self):
        self.config_path = "./config/app.cfg"
        self.config = None

        self.short_url_len = None
        self.host = None
        self.port = None
        self.base_url = None
        self.db_name = None
        self.db_echo = True

        self.initialize()

    def load_config(self):
        self.config = ConfigParser()
        self.config.read(self.config_path)
        
    def initialize(self):
        self.load_config()

        self.host = self.config['server']['host']
        self.short_url_len = self.config['url_shortener']['length']
        self.port = self.config['server']['port']
        self.base_url = self.config['server']['base_url']
        self.db_name = self.config['db']['db_name']

        if self.config['environment']['env'] == 'prod':
            self.db_echo = False

