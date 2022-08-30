from typing import Dict
import os
import toml

default_config = {
    'min-channel-size-sat': -1,  # -1 equals not set
    'allow-tor-only-nodes': True,
    'strict-tor-only-node-check': False
}


class ChannelAcceptorConfig:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.public_config, self.private_config = self.merge_configs(config)

    def merge_configs(self, config: Dict):

        user_general = config.get('general', {})
        user_public = config.get('public_channels', {})
        user_private = config.get('private_channels', {})

        public_config = {**default_config, **user_general, **user_public}
        private_config = {**default_config, **user_general, **user_private}
        return public_config, private_config

    @classmethod
    def load_from_toml(cls, path) -> 'ChannelAcceptorConfig':
        if os.path.exists(path):
            with open(path) as file:
                config = toml.loads(file.read())
        else:
            config = {}
        return ChannelAcceptorConfig(config)
