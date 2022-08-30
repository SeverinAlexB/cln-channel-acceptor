from typing import List, Dict

'''
{
     "nodeid": "027ce055380348d7812d2ae7745701c9f93e70c1adeb2657f053f91df4f2843c71",
     "alias": "c-otto.de",
     "color": "3399ff",
     "last_timestamp": 1661292582,
     "features": "800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000802000888a52a1",
     "addresses": [
        {
           "type": "ipv4",
           "address": "157.90.112.145",
           "port": 9735
        },
        {
           "type": "ipv6",
           "address": "2a01:4f8:c2c:e8a0::1",
           "port": 9735
        },
        {
           "type": "torv3",
           "address": "yi6ccghmivsydduxb2wnogyx2chz347bgu3kvqefea7rnhfi5iifqcyd.onion",
           "port": 9735
        }
     ]
  }
'''

class GraphNodeAddress:
    def __init__(self, data):
        self.type: str = data['type']
        self.address: str = data['address']
        self.port: int = data['port']

    @property
    def is_ip(self):
        return self.type.startswith('ip')


class GraphNode:
    def __init__(self, data: Dict):
        self.node_id: str = data['nodeid']
        self.alias: str = data['alias']
        self.addresses: List[GraphNodeAddress] = []
        if 'addresses' in data:
            for address in data['addresses']:
                self.addresses.append(GraphNodeAddress(address))

    @property
    def has_ip_address(self) -> bool:
        for address in self.addresses:
            if address.is_ip:
                return True
        return False


