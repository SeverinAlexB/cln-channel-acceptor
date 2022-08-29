from typing import Dict
import os
import toml


class ChannelAcceptorConfig:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.public_config, self.private_config = self.merge_configs(config)

    def load_default_config(self) -> Dict:
        path = os.path.dirname(os.path.realpath(__file__)) + '/default_config.toml'
        with open(path) as file:
            return toml.loads(file.read())

    def merge_configs(self, config: Dict):
        default_config = self.load_default_config()
        user_general = config.get('general', {})
        user_public = config.get('public_channels', {})
        user_private = config.get('private_channels', {})

        default_general = default_config.get('general', {})
        default_public = default_config.get('public_channels', {})
        default_private = default_config.get('private_channels', {})

        public_config = {**default_general, **default_public, **user_general, **user_public}
        private_config = {**default_general, **default_private, **user_general, **user_private}
        return public_config, private_config

    @classmethod
    def load_from_toml(cls, path) -> 'ChannelAcceptorConfig':
        if os.path.exists(path):
            with open(path) as file:
                config = toml.loads(file.read())
        else:
            config = {}
        return ChannelAcceptorConfig(config)
