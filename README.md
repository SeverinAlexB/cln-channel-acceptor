# cln-channel-acceptor

[CLN](https://github.com/ElementsProject/lightning) plugin to control who can establish a channel to your node
and what parameters they use. 

Current path finding algorithms have limitations. If you want to be a performant routing node you should vet
the nodes that open channels to you.

## Install & Usage

```bash
git clone https://github.com/SeverinAlexB/cln-channel-acceptor
cd cln-channel-acceptor
pip3 install -r requirements.txt
cd ~/.lightning/plugins        # Create the plugin folder if it doesn't exist yet.
ln -s %PathToClonedGit%/channel_acceptor.py channel_acceptor.py 
```

Restart your lightning node to start the plugin or reload the settings.

### Configure

The acceptor can be configured with a configuration file `.lightning/channel_acceptor.yaml`.
A sample configuration is given here:

```yaml
general:
  min_channel_size_sat: 100000       # Every channel opened needs to be at least 100,000sat

public_channels:
  allow_tor_only_nodes: false        # Do not allow tor-only nodes to open public channels.
  min_channel_size_sat: 5000000      # Every public channel needs to be at least 5M sat.


private_channels:
  allow_tor_only_nodes: true         # Allow private channels from tor-only nodes.
```

**Sections**

- `general` Applies to private and public channels.
- `public_channels` Applies to public channels only. Overrides the general settings.
- `private_channels` Applies to private channels only. Overrides the general settings.


**Settings**

- `min_channel_size_sat` Default: -1. Minimal channel size in satoshi. -1 means the setting is not applied.
- `allow_tor_only_nodes` Default: true. A tor-only node only has Tor addresses and no IP addresses announced. If false
prevents tor-only nodes to establish a channel.
- `strict_tor_only_node_check` Default: false. The acceptor looks up the node address in the graph. If the node can't 
be found and therefore the addresses can't be determined, it rejects the node.
- `dev_mode` Default: false. In general section only. Rejects all incoming channels. Logs the result of the acceptor in
to logs.


## Development

Change the parameters of the following command to mount the Lighting RPC file from a server to your local machine via ssh.

```bash
rm -rf $HOME/.lightning/lightning-rpc && ssh -nNT -L $HOME/.lightning/lightning-rpc:/home/bitcoin/.lightning/bitcoin/lightning-rpc your.server.com
```
