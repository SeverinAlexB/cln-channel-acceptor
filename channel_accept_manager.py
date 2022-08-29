from typing import Dict

from lightning import LightningRpc

from channel_acceptor_config import ChannelAcceptorConfig


class ChannelAcceptManager:
    def __init__(self, lightning_rpc_path: str, config: ChannelAcceptorConfig):
        self.rpc: LightningRpc = LightningRpc(lightning_rpc_path)
        self.getinfo = self.rpc.getinfo()
        self.config: ChannelAcceptorConfig = config

    @property
    def my_node_id(self):
        return self.getinfo['id']
