from dataclasses import dataclass

@dataclass(frozen=True, repr=True)
class Transaction:
    datetime: str
    sender: str
    recipient: str
    amount: float
    hash_id: str
    memo: str

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, 'datetime', str(kwargs['datetime']))
        object.__setattr__(self, 'sender', str(kwargs['sender']))
        object.__setattr__(self, 'recipient', str(kwargs['recipient']))
        object.__setattr__(self, 'amount', float(kwargs['amount']))
        object.__setattr__(self, 'hash_id', str(kwargs['hash']))
        object.__setattr__(self, 'memo', str(kwargs['memo']))

    def __eq__(self, o):
        if not isinstance(o, Transaction):
            return False
        return self.hash_id == o.hash_id