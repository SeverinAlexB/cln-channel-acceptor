#!/usr/bin/env python3
from lightning import Plugin
import os

from channel_accept_manager import ChannelAcceptManager

''' Configuration example
{'lightning-dir': '/home/bitcoin/.lightning/bitcoin', 'rpc-file': 'lightning-rpc', 'startup': True, 'network': 'bitcoin', 'feature_set': {'init': '080269a2', 'node': '800000080269a2', 'channel': '', 'invoice': '02000000024100'}}
2022-08-29T14:18:00.789Z INFO    lightningd: Peer says it sees our address as: 159.69.208.81:36252
'''

plugin = Plugin()
acceptor: ChannelAcceptManager

@plugin.init()
def init(options, configuration, plugin):
    rpc_url = configuration['lightning-dir'] + '/' + configuration['rpc-file']
    global acceptor
    acceptor = ChannelAcceptManager(rpc_url, {})
    plugin.log("Plugin channelacceptor.py initialized: " + os.path.realpath(__file__))





plugin.run()