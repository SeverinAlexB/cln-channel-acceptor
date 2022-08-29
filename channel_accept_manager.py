from typing import Dict

from lightning import LightningRpc


class ChannelAcceptManager:
    def __init__(self, lightning_rpc_path: str, config: Dict):
        self.rpc: LightningRpc = LightningRpc(lightning_rpc_path)
        self.getinfo = self.rpc.getinfo()
        self.config: Dict = config

    @property
    def my_node_id(self):
        return self.getinfo['id']
