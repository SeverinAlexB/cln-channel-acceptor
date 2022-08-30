#!/usr/bin/env python3
import json

from pyln.client import Plugin
import os
from src.channel_accept_manager import ChannelAcceptManager
from src.channel_acceptor_config import ChannelAcceptorConfig
from src.channel_open_request import OpenChannelRequestV1, OpenChannelRequestV2

''' Configuration example
{'lightning-dir': '/home/bitcoin/.lightning/bitcoin', 'rpc-file': 'lightning-rpc', 'startup': True, 'network': 'bitcoin', 'feature_set': {'init': '080269a2', 'node': '800000080269a2', 'channel': '', 'invoice': '02000000024100'}}
2022-08-29T14:18:00.789Z INFO    lightningd: Peer says it sees our address as: 159.69.208.81:36252
'''

plugin = Plugin()
acceptor: ChannelAcceptManager
DEV_MODE = False  # Rejects all channels if set to true

@plugin.init()
def init(options, configuration, plugin):
    config_toml_path = configuration['lightning-dir'] + '/channel_acceptor.toml'
    plugin.log('Load config from ' + config_toml_path)
    if not os.path.exists(config_toml_path):
        plugin.log('- Config file not found.')
    config = ChannelAcceptorConfig.load_from_toml(config_toml_path)

    global DEV_MODE
    DEV_MODE = config.user_config.get('general', {}).get('dev_mode', False)
    if DEV_MODE:
        plugin.log('Run in DEV_MODE. Rejects all channels.')

    rpc_url = configuration['lightning-dir'] + '/' + configuration['rpc-file']
    global acceptor
    acceptor = ChannelAcceptManager(rpc_url, config)
    plugin.log("Plugin channel_acceptor.py initialized.")


@plugin.method("listchannelacceptorconfig")
def list_channel_acceptor_config(plugin):
    """Lists the configuration for the channel acceptor plugin."""
    config = {
        'public-channels': acceptor.config.public_config,
        'private-channels': acceptor.config.private_config
    }
    s = json.dumps(config, indent=2)
    s = s.replace('\n', '\\n')
    plugin.log(s)

    return s


@plugin.hook("openchannel")
def on_openchannel(plugin, openchannel, **kwargs):
    plugin.log("Received openchannel event.")
    plugin.log(str(openchannel))

    request = OpenChannelRequestV1.from_openchannel_hook(openchannel)
    should_accept, reason = acceptor.should_accept(request)
    plugin.log(f"Should accept: {should_accept}, reason: {reason}")

    if DEV_MODE:
        return {
            "result": "reject"
        }

    if should_accept:
        return {
            "result": "continue"
        }

    return {
            "result": "reject"
        }


@plugin.hook("openchannel2")
def on_openchannel2(plugin, openchannel2, **kwargs):
    plugin.log("Received openchannel2 event.")
    plugin.log(str(openchannel2))

    request = OpenChannelRequestV2.from_openchannel2_hook(openchannel2)
    should_accept, reason = acceptor.should_accept(request)
    plugin.log(f"Should accept: {should_accept}, reason: {reason}")

    if DEV_MODE:
        return {
            "result": "reject",
            "error_message": "ChannelAcceptor DEV_MODE. Reject all channels."
        }

    if should_accept:
        return {
            "result": "continue",
        }

    return {
        "result": "reject",
        "error_message": reason
    }


plugin.run()

