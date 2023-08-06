from dataclasses import dataclass

@dataclass(frozen=True, repr=True)
class Miner:
    threadid: str
    username: str
    hashrate: int
    sharetime: float
    accepted: int
    rejected: int
    diff: int
    software: str
    identifier: str
    algorithm: str

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, 'threadid', str(kwargs['threadid']))
        object.__setattr__(self, 'username', str(kwargs['username']))
        object.__setattr__(self, 'hashrate', int(kwargs['hashrate']))
        object.__setattr__(self, 'sharetime', float(kwargs['sharetime']))
        object.__setattr__(self, 'accepted', int(kwargs['accepted']))
        object.__setattr__(self, 'rejected', int(kwargs['rejected']))
        object.__setattr__(self, 'diff', int(kwargs['diff']))
        object.__setattr__(self, 'software', str(kwargs['software']))
        object.__setattr__(self, 'identifier', str(kwargs['identifier']))
        object.__setattr__(self, 'algorithm', str(kwargs['algorithm']))

    def __eq__(self, o):
        if not isinstance(o, Miner):
            return False
        return self.threadid == o.threadid