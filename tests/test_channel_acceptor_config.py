import unittest
import os.path
from channel_accept_manager import ChannelAcceptManager
from channel_acceptor_config import ChannelAcceptorConfig

'''
Make sure you establish an RPC connection to run the test. 
The test should be readonly and not modify anything!!!
'''


class TestChannelAcceptorConfigMethod(unittest.TestCase):

    def test_public_channel(self):
        config = ChannelAcceptorConfig({'public_channels': {'min-channel-size': 5}})
        self.assertEqual(config.public_config['min-channel-size'], 5)

    def test_default_values(self):
        config = ChannelAcceptorConfig()
        self.assertEqual(config.private_config['min-channel-size'], -1)

    def test_private_values(self):
        config = ChannelAcceptorConfig()
        self.assertEqual(config.private_config['allow-tor'], True)
