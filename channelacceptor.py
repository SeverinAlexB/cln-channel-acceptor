#!/usr/bin/env python3
from lightning import Plugin


plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("Plugin channelacceptor.py initialized")
    plugin.log("Options: " + str(options))
    plugin.log("Configuration: " + str(configuration))

plugin.run()