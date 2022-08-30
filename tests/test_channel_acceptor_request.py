import unittest
import os.path
from channel_accept_manager import ChannelAcceptManager
from channel_acceptor_config import ChannelAcceptorConfig
from channel_open_request import OpenChannelRequestV1, OpenChannelRequestV2

'''
Make sure you establish an RPC connection to run the test. 
The test should be readonly and not modify anything!!!
'''


class TestChannelAcceptorRequest(unittest.TestCase):

    def test_v1(self):
        data = {
            "id": "03a7d3d1c70b0782ca2640e9db81a820d3f682eff92cb0ee319f3b793a0455f7f4",
            "funding_satoshis": "10000000msat",
            "push_msat": "0msat",
            "dust_limit_satoshis": "546000msat",
            "max_htlc_value_in_flight_msat": "18446744073709551615msat",
            "channel_reserve_satoshis": "546000msat",
            "htlc_minimum_msat": "0msat",
            "feerate_per_kw": 253,
            "to_self_delay": 144,
            "max_accepted_htlcs": 30,
            "channel_flags": 1
        }
        req = OpenChannelRequestV1.from_openchannel_hook(data)
        self.assertEqual(req.id, '03a7d3d1c70b0782ca2640e9db81a820d3f682eff92cb0ee319f3b793a0455f7f4')
        self.assertEqual(req.funding_satoshis, 10000)
        self.assertEqual(req.push_msat, 0)
        self.assertEqual(req.dust_limit_msat, 546000)
        self.assertEqual(req.max_htlc_value_in_flight_msat, 18446744073709551615)
        self.assertEqual(req.channel_reserve_satoshis, 546)
        self.assertEqual(req.htlc_minimum_msat, 0)
        self.assertEqual(req.feerate_per_kw, 253)
        self.assertEqual(req.to_self_delay, 144)
        self.assertEqual(req.max_accepted_htlcs, 30)
        self.assertEqual(req.channel_flags, 1)

        self.assertFalse(req.is_private)
        self.assertEqual(req.channel_size_sat, 10000)

    def test_v2(self):
        data = {
            "id": "03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f",
            "channel_id": "252d1b0a1e57895e84137f28cf19ab2c35847e284c112fefdecc7afeaa5c1de7",
            "their_funding_msat": 100000000,
            "dust_limit_msat": 546000,
            "max_htlc_value_in_flight_msat": 18446744073709551615,
            "htlc_minimum_msat": 0,
            "funding_feerate_per_kw": 7500,
            "commitment_feerate_per_kw": 7500,
            "feerate_our_max": 10000,
            "feerate_our_min": 253,
            "to_self_delay": 5,
            "max_accepted_htlcs": 483,
            "channel_flags": 1,
            "locktime": 2453,
            "channel_max_msat": 16777215000,
            "requested_lease_msat": 100000000,
            "lease_blockheight_start": 683990,
            "node_blockheight": 683990
        }
        req = OpenChannelRequestV2.from_openchannel2_hook(data)
        self.assertEqual(req.id, '03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f')
        self.assertEqual(req.channel_id, '252d1b0a1e57895e84137f28cf19ab2c35847e284c112fefdecc7afeaa5c1de7')
        self.assertEqual(req.their_funding_msat, 100000000)
        self.assertEqual(req.dust_limit_msat, 546000)
        self.assertEqual(req.max_htlc_value_in_flight_msat, 18446744073709551615)
        self.assertEqual(req.htlc_minimum_msat, 0)
        self.assertEqual(req.funding_feerate_per_kw,7500 )
        self.assertEqual(req.commitment_feerate_per_kw, 7500)
        self.assertEqual(req.feerate_our_max, 10000)
        self.assertEqual(req.feerate_our_min, 253)
        self.assertEqual(req.to_self_delay, 5)
        self.assertEqual(req.max_accepted_htlcs, 483)
        self.assertEqual(req.channel_flags, 1)
        self.assertEqual(req.locktime, 2453)
        self.assertEqual(req.channel_max_msat, 16777215000)
        self.assertEqual(req.requested_lease_msat, 100000000)
        self.assertEqual(req.lease_blockheight_start, 683990)
        self.assertEqual(req.node_blockheight, 683990)

        self.assertFalse(req.is_private)
        self.assertEqual(req.channel_size_sat, 200000)
