#!/usr/bin/env python3
import json

from pyln.client import Plugin
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


@plugin.method("listchannelacceptorconfig")
def list_channel_acceptor_config(plugin):
    """Lists the configuration for the channel acceptor plugin."""
    config = {
        'public-channels': acceptor.config.public_config,
        'private-channels': acceptor.config.private_config
    }
    s = str(config)  #json.dumps(config, indent=2)
    plugin.log(s)

    return s


@plugin.hook("openchannel")
def on_openchannel(plugin, **kwargs):
    plugin.log("Received openchannel event.")
    plugin.log(kwargs)
    return {
        "result": "reject"
    }


@plugin.hook("openchannel2")
def on_openchannel2(plugin, **kwargs):
    plugin.log("Received openchannel2 event.")
    plugin.log(kwargs)
    return {
        "result": "reject",
        "error_message": "ChannelAcceptor: Channel rejected"
    }


plugin.run()

