#!/usr/bin/env python3
from lightning import Plugin
import os
from channel_accept_manager import ChannelAcceptManager
from channel_acceptor_config import ChannelAcceptorConfig

''' Configuration example
{'lightning-dir': '/home/bitcoin/.lightning/bitcoin', 'rpc-file': 'lightning-rpc', 'startup': True, 'network': 'bitcoin', 'feature_set': {'init': '080269a2', 'node': '800000080269a2', 'channel': '', 'invoice': '02000000024100'}}
2022-08-29T14:18:00.789Z INFO    lightningd: Peer says it sees our address as: 159.69.208.81:36252
'''

plugin = Plugin()
acceptor: ChannelAcceptManager



@plugin.init()
def init(options, configuration, plugin):
    config_toml_path = configuration['lightning-dir'] + '/channelacceptor.toml'
    if os.path.exists(config_toml_path):
        plugin.log('Load config from ' + config_toml_path)
    config = ChannelAcceptorConfig.load_from_toml(config_toml_path)

    rpc_url = configuration['lightning-dir'] + '/' + configuration['rpc-file']
    global acceptor
    acceptor = ChannelAcceptManager(rpc_url, config)
    plugin.log("Plugin channelacceptor.py initialized.")


@plugin.method("list-channel-acceptor-config")
def list_channel_acceptor_config(plugin):
    s = 'Public channels: ' + str(acceptor.config.public_config) + '\n'
    s += 'Private channels: ' + str(acceptor.config.public_config)

    plugin.log(s)
    return s


plugin.run()