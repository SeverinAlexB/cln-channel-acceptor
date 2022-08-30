from typing import Union

'''
{
  "id":"03a7d3d1c70b0782ca2640e9db81a820d3f682eff92cb0ee319f3b793a0455f7f4",
  *"funding_satoshis":"10000000msat",
  *"push_msat":"0msat",
  "dust_limit_satoshis":"546000msat",
  "max_htlc_value_in_flight_msat":"18446744073709551615msat",
  *"channel_reserve_satoshis":"546000msat",
  "htlc_minimum_msat":"0msat",
  *"feerate_per_kw":253,
  "to_self_delay":144,
  "max_accepted_htlcs":30,
  "channel_flags":1
}
'''
'''
{
    "id": "03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f",
    *"channel_id": "252d1b0a1e57895e84137f28cf19ab2c35847e284c112fefdecc7afeaa5c1de7",
    *"their_funding_msat": 100000000,
    "dust_limit_msat": 546000,
    "max_htlc_value_in_flight_msat": 18446744073709551615,
    *"htlc_minimum_msat": 0,
    *"funding_feerate_per_kw": 7500,
    *"commitment_feerate_per_kw": 7500,
    *"feerate_our_max": 10000,
    *"feerate_our_min": 253,
    "to_self_delay": 5,
    "max_accepted_htlcs": 483,
    "channel_flags": 1
    *"locktime": 2453,
    *"channel_max_msat": 16777215000,
    *"requested_lease_msat": 100000000,
    *"lease_blockheight_start": 683990,
    *"node_blockheight": 683990
  }
'''



class AbstractChannelOpenRequest:
    def __init__(self):
        self.id: str = None # Node id
        self.dust_limit_msat: int = None
        self.max_htlc_value_in_flight_msat: int = None
        self.htlc_minimum_msat: int = None
        self.to_self_delay: int = None
        self.max_accepted_htlcs: int = None
        self.channel_flags: int = None

    @property
    def is_private(self) -> bool:
        if not (self.channel_flags == 0 or self.channel_flags == 1):
            # Sanity check in case cln added a new channel flag that is unknown.
            raise Exception("Unknown channel flag " + str(self.channel_flags))

        return self.channel_flags == 0

    @property
    def channel_size_sat(self) -> int:
        raise NotImplementedError()


class OpenChannelRequestV1(AbstractChannelOpenRequest):
    def __init__(self):
        super().__init__()
        self.funding_satoshis: int = None
        self.push_msat: int = None
        self.channel_reserve_satoshis: int = None
        self.feerate_per_kw: int = None

    @property
    def channel_size_sat(self) -> int:
        return self.funding_satoshis

    @staticmethod
    def _msat_str_to_int(msat:str) -> int:
        return int(str(msat).replace("msat", ""))

    @classmethod
    def from_openchannel_hook(cls, data: any) -> 'OpenChannelRequestV1':
        '''
        {
          "id":"03a7d3d1c70b0782ca2640e9db81a820d3f682eff92cb0ee319f3b793a0455f7f4",
          "funding_satoshis":"10000000msat",
          "push_msat":"0msat",
          "dust_limit_satoshis":"546000msat",
          "max_htlc_value_in_flight_msat":"18446744073709551615msat",
          "channel_reserve_satoshis":"546000msat",
          "htlc_minimum_msat":"0msat",
          "feerate_per_kw":253,
          "to_self_delay":144,
          "max_accepted_htlcs":30,
          "channel_flags":1
        }
        '''

        req = cls()
        req.id = data['id']
        req.funding_satoshis = cls._msat_str_to_int(data['funding_satoshis'])/1000
        req.push_msat = cls._msat_str_to_int(data['push_msat'])
        req.dust_limit_msat = cls._msat_str_to_int(data['dust_limit_satoshis'])
        req.max_htlc_value_in_flight_msat = cls._msat_str_to_int(data['max_htlc_value_in_flight_msat'])
        req.channel_reserve_satoshis = cls._msat_str_to_int(data['channel_reserve_satoshis']) / 1000
        req.htlc_minimum_msat = cls._msat_str_to_int(data['htlc_minimum_msat'])
        req.feerate_per_kw = data['feerate_per_kw']
        req.to_self_delay = data['to_self_delay']
        req.max_accepted_htlcs = data['max_accepted_htlcs']
        req.channel_flags = data['channel_flags']
        return req


class OpenChannelRequestV2(AbstractChannelOpenRequest):
    def __init__(self):
        super().__init__()
        self.channel_id: str = None
        self.their_funding_msat: int = None
        self.htlc_minimum_msat: int = None
        self.funding_feerate_per_kw: int = None
        self.commitment_feerate_per_kw: int = None
        self.feerate_our_max: int = None
        self.feerate_our_min: int = None
        self.locktime: int = None
        self.channel_max_msat: int = None
        self.requested_lease_msat: int = None
        self.lease_blockheight_start: int = None
        self.node_blockheight: int = None

    @property
    def channel_size_sat(self) -> int:
        return int((self.their_funding_msat + self.requested_lease_msat)/1000)


    @classmethod
    def from_openchannel2_hook(cls, data: any) -> 'OpenChannelRequestV2':
        '''
        {
            "id": "03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f",
            *"channel_id": "252d1b0a1e57895e84137f28cf19ab2c35847e284c112fefdecc7afeaa5c1de7",
            *"their_funding_msat": 100000000,
            "dust_limit_msat": 546000,
            "max_htlc_value_in_flight_msat": 18446744073709551615,
            *"htlc_minimum_msat": 0,
            *"funding_feerate_per_kw": 7500,
            *"commitment_feerate_per_kw": 7500,
            *"feerate_our_max": 10000,
            *"feerate_our_min": 253,
            "to_self_delay": 5,
            "max_accepted_htlcs": 483,
            "channel_flags": 1
            *"locktime": 2453,
            *"channel_max_msat": 16777215000,
            *"requested_lease_msat": 100000000,
            *"lease_blockheight_start": 683990,
            *"node_blockheight": 683990
        }
        '''

        req = cls()
        req.id = data['id']
        req.channel_id = data['channel_id']
        req.their_funding_msat = data['their_funding_msat']
        req.dust_limit_msat = data['dust_limit_msat']
        req.max_htlc_value_in_flight_msat = data['max_htlc_value_in_flight_msat']
        req.htlc_minimum_msat = data['htlc_minimum_msat']
        req.funding_feerate_per_kw = data['funding_feerate_per_kw']
        req.commitment_feerate_per_kw = data['commitment_feerate_per_kw']
        req.feerate_our_max = data['feerate_our_max']
        req.feerate_our_min = data['feerate_our_min']
        req.to_self_delay = data['to_self_delay']
        req.max_accepted_htlcs = data['max_accepted_htlcs']
        req.channel_flags = data['channel_flags']
        req.locktime = data['locktime']
        req.channel_max_msat = data['channel_max_msat']
        req.requested_lease_msat = data['requested_lease_msat']
        req.lease_blockheight_start = data['lease_blockheight_start']
        req.node_blockheight = data['node_blockheight']

        return req
