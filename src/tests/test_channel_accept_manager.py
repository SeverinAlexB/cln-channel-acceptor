import unittest
import os.path
from src.channel_accept_manager import ChannelAcceptManager
from src.channel_acceptor_config import ChannelAcceptorConfig
from src.channel_open_request import OpenChannelRequestV1

'''
Make sure you establish an RPC connection to run the test. 
The test should be readonly and not modify anything!!!
'''


class TestChannelAcceptManagerMethod(unittest.TestCase):

    def test_rpc_connection(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path, ChannelAcceptorConfig())
        node_id = acceptor.my_node_id
        self.assertEqual(len(node_id), 66)

    def test_min_channel_size_fail(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path, ChannelAcceptorConfig({
            'private_channels': {
                'min_channel_size_sat': 1000
            }
        }))

        request = OpenChannelRequestV1.from_openchannel_hook({
            # yalls.org yalls-tor - At the time, this is a tor only node
            "id": "03d06758583bb5154774a6eb221b1276c9e82d65bbaceca806d90e20c108f4b1c7",
            "funding_satoshis": "10000msat",  # 10sat
            "push_msat": "0msat",
            "dust_limit_satoshis": "546000msat",
            "max_htlc_value_in_flight_msat": "18446744073709551615msat",
            "channel_reserve_satoshis": "546000msat",
            "htlc_minimum_msat": "0msat",
            "feerate_per_kw": 253,
            "to_self_delay": 144,
            "max_accepted_htlcs": 30,
            "channel_flags": 0
        })

        should_accept, reason = acceptor.should_accept(request)
        self.assertEqual(should_accept, False)

    def test_min_channel_size_success(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path, ChannelAcceptorConfig({
            'private_channels': {
                'min_channel_size_sat': 1000
            }
        }))

        request = OpenChannelRequestV1.from_openchannel_hook({
            # yalls.org yalls-tor - At the time, this is a tor only node
            "id": "03d06758583bb5154774a6eb221b1276c9e82d65bbaceca806d90e20c108f4b1c7",
            "funding_satoshis": "1000000msat",  # 10sat
            "push_msat": "0msat",
            "dust_limit_satoshis": "546000msat",
            "max_htlc_value_in_flight_msat": "18446744073709551615msat",
            "channel_reserve_satoshis": "546000msat",
            "htlc_minimum_msat": "0msat",
            "feerate_per_kw": 253,
            "to_self_delay": 144,
            "max_accepted_htlcs": 30,
            "channel_flags": 0
        })

        should_accept, reason = acceptor.should_accept(request)
        self.assertEqual(should_accept, True)

    def test_allow_tor_only_fail(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path, ChannelAcceptorConfig({
            'general': {
                'allow_tor_only_nodes': False
            }
        }))

        request = OpenChannelRequestV1.from_openchannel_hook({
            # yalls.org yalls-tor - At the time, this is a tor only node
            "id": "03d06758583bb5154774a6eb221b1276c9e82d65bbaceca806d90e20c108f4b1c7",
            "funding_satoshis": "10000msat",  # 10sat
            "push_msat": "0msat",
            "dust_limit_satoshis": "546000msat",
            "max_htlc_value_in_flight_msat": "18446744073709551615msat",
            "channel_reserve_satoshis": "546000msat",
            "htlc_minimum_msat": "0msat",
            "feerate_per_kw": 253,
            "to_self_delay": 144,
            "max_accepted_htlcs": 30,
            "channel_flags": 0
        })

        should_accept, reason = acceptor.should_accept(request)
        self.assertEqual(should_accept, False)

    def test_allow_tor_only_success(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path, ChannelAcceptorConfig({
            'public_channels': {
                'allow_tor_only_nodes': True
            },
            'general': {
                'allow_tor_only_nodes': False
            }
        }))

        request = OpenChannelRequestV1.from_openchannel_hook({
            # yalls.org clearnet-yalls - At the time, this is a clearnet only node
            "id": "0288be11d147e1525f7f234f304b094d6627d2c70f3313d7ba3696887b261c4447",
            "funding_satoshis": "10000msat",  # 10sat
            "push_msat": "0msat",
            "dust_limit_satoshis": "546000msat",
            "max_htlc_value_in_flight_msat": "18446744073709551615msat",
            "channel_reserve_satoshis": "546000msat",
            "htlc_minimum_msat": "0msat",
            "feerate_per_kw": 253,
            "to_self_delay": 144,
            "max_accepted_htlcs": 30,
            "channel_flags": 1
        })

        should_accept, reason = acceptor.should_accept(request)
        self.assertEqual(should_accept, True)

