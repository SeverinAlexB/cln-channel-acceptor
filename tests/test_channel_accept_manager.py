import unittest
import os.path
from channel_accept_manager import ChannelAcceptManager

'''
Make sure you establish an RPC connection to run the test. 
The test should be readonly and not modify anything!!!
'''


class TestChannelAcceptManagerMethod(unittest.TestCase):

    def test_rpc_connection(self):
        rpc_path = os.path.expandvars('$HOME/.lightning/lightning-rpc')
        acceptor = ChannelAcceptManager(rpc_path)
        node_id = acceptor.my_node_id
        self.assertEqual(len(node_id), 66)

