from typing import Dict, Union, Tuple

from lightning import LightningRpc

from channel_acceptor_config import ChannelAcceptorConfig
from channel_open_request import AbstractChannelOpenRequest
from graph_node import GraphNode


class ChannelAcceptManager:
    def __init__(self, lightning_rpc_path: str, config: ChannelAcceptorConfig):
        self.rpc: LightningRpc = LightningRpc(lightning_rpc_path)
        self.getinfo = self.rpc.getinfo()
        self.config: ChannelAcceptorConfig = config

    @property
    def my_node_id(self):
        return self.getinfo['id']

    def _is_tor_only_node(self, node_id: str, strict_tor_check: bool) -> bool:
        node_data = self.rpc.listnodes(node_id)

        node_not_found = len(node_data['nodes']) == 0
        if node_not_found:
            return strict_tor_check

        graph_node = GraphNode(node_data['nodes'][0])
        return not graph_node.has_ip_address

    def should_accept(self, request: AbstractChannelOpenRequest) -> Tuple[bool, str]:
        """
        Checks if the request matches the given config.
        :param request: Channel request class
        :return: accept: bool, reason: str
        """
        config = self.config.private_config if request.is_private else self.config.public_config

        if not config['min_channel_size_sat'] < 0 and request.channel_size_sat < config['min_channel_size_sat']:
            return False, "Channel below " + str(config['min_channel_size_sat']) + "sat."

        if not config['allow_tor_only_nodes']:
            is_tor_only = self._is_tor_only_node(request.id, config['strict_tor_only_node_check'])
            if is_tor_only:
                return False, "Tor only nodes are not allowed."

        return True, "Ok"


