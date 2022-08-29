# cln-channel-acceptor


## Development

Change the parameters of the following command to mount the Lighting RPC file from a server to your local machine via ssh.

```bash
rm -rf $HOME/.lightning/lightning-rpc && ssh -nNT -L $HOME/.lightning/lightning-rpc:/home/bitcoin/.lightning/bitcoin/lightning-rpc your.server.com
```