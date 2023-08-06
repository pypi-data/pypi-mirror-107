import requests
import yaml
from common_structure_microservices.exception import GenericMicroserviceError


class Profiles:
    file_config = yaml.load(open('profile.yaml'))['django']
    APP_NAME = file_config['application']['NAME']
    PROFILE = file_config['profiles']['active']
    ENVIRONMENTS = f'{APP_NAME}-{PROFILE}.yml'
    URI = file_config['cloud']['config']['uri'] + ENVIRONMENTS
    CONFIG = {}
    env = {}
    APPLICATION = {}

    def get_env(self):
        try:
            r = requests.get(self.URI, allow_redirects=True)
            open(self.ENVIRONMENTS, 'wb').write(r.content)
            self.env = yaml.load(open(self.ENVIRONMENTS))['django']
            self.CONFIG = self.env['cloud']['config']
            self.APPLICATION = self.env['application']
            print('IMPORTANT -> ' + self.ENVIRONMENTS)
        except Exception as e:
            raise GenericMicroserviceError(status=500, detail=f'ERROR CONFIG ENV: {e}')
