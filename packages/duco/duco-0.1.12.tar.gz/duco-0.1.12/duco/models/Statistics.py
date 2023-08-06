from dataclasses import dataclass
from typing import List

@dataclass(frozen=True, repr=True)
class Statistics:
    active_connections: int
    active_workers: dict
    all_time_mined_duco: float
    current_difficulty: int
    ducos1_hashrate: str
    duco_justswap_price: float
    duco_nodes_price: float
    duco_price_usd: float
    duinocoin_server_api: str
    last_block_hash: str
    last_update: str
    mined_blocks: int
    miners: str
    open_threads: int
    pool_hashrate: str
    registered_users: int
    server_cpu_usage: float
    server_ram_usage: float
    server_version: float
    top_10_richest_miners: List[str]
    xxhash_hashrate: str

    def __init__(self, **kwargs):
        object.__setattr__(self, 'active_connections', str(kwargs['Active connections']))
        object.__setattr__(self, 'active_workers', dict(kwargs['Active workers']))
        object.__setattr__(self, 'all_time_mined_duco', float(kwargs['All-time mined DUCO']))
        object.__setattr__(self, 'current_difficulty', int(kwargs['Current difficulty']))
        object.__setattr__(self, 'ducos1_hashrate', str(kwargs['DUCO-S1 hashrate']))
        object.__setattr__(self, 'duco_justswap_price', float(kwargs['Duco JustSwap price']))
        object.__setattr__(self, 'duco_nodes_price', float(kwargs['Duco Node-S price']))
        object.__setattr__(self, 'duco_price_usd', float(kwargs['Duco price']))
        object.__setattr__(self, 'duinocoin_server_api', str(kwargs['Duino-Coin Server API']))
        object.__setattr__(self, 'last_block_hash', str(kwargs['Last block hash']))
        object.__setattr__(self, 'last_update', str(kwargs['Last update']))
        object.__setattr__(self, 'mined_blocks', str(kwargs['Mined blocks']))
        object.__setattr__(self, 'miners', str(kwargs['Miners']))
        object.__setattr__(self, 'open_threads', int(kwargs['Open threads']))
        object.__setattr__(self, 'pool_hashrate', str(kwargs['Pool hashrate']))
        object.__setattr__(self, 'registered_users', int(kwargs['Registered users']))
        object.__setattr__(self, 'server_cpu_usage', float(kwargs['Server CPU usage']))
        object.__setattr__(self, 'server_ram_usage', float(kwargs['Server RAM usage']))
        object.__setattr__(self, 'server_version', float(kwargs['Server version']))
        object.__setattr__(self, 'top_10_richest_miners', list(kwargs['Top 10 richest miners']))
        object.__setattr__(self, 'xxhash_hashrate', str(kwargs['XXHASH hashrate']))

