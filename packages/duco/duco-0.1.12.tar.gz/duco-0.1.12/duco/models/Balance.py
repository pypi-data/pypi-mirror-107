from dataclasses import dataclass

@dataclass(frozen=True, repr=True)
class Balance:
    username: str
    balance: float

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, 'username', str(kwargs['username']))
        object.__setattr__(self, 'balance', float(kwargs['balance']))
        
    def __eq__(self, o):
        if not isinstance(o, Balance):
            return False
        return self.username == o.username