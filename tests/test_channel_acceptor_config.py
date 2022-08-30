import unittest
from channel_acceptor_config import ChannelAcceptorConfig

'''
Make sure you establish an RPC connection to run the test. 
The test should be readonly and not modify anything!!!
'''


class TestChannelAcceptorConfigMethod(unittest.TestCase):

    def test_public_channel(self):
        config = ChannelAcceptorConfig({'public_channels': {'min_channel_size_sat': 5}})
        self.assertEqual(config.public_config['min_channel_size_sat'], 5)

    def test_default_values(self):
        config = ChannelAcceptorConfig()
        self.assertEqual(config.private_config['min_channel_size_sat'], -1)

    def test_private_values(self):
        config = ChannelAcceptorConfig()
        self.assertEqual(config.private_config['allow_tor_only_nodes'], True)
