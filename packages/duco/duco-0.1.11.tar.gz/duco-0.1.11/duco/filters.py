from dataclasses import dataclass, field

@dataclass(frozen=True)
class Comparative:
    EQUAL: str = ''
    LESS_THAN: str = 'lt'
    LESS_THAN_OR_EQUAL: str = 'lte'
    GREATER_THAN: str = 'gt'
    GREATER_THAN_OR_EQUAL: str = 'gte'
    NOT_EQUAL: str = 'ne'

@dataclass(frozen=True)
class SortDirection:
    ASCENDING: str = 'asc'
    DESCENDING: str = 'desc'

@dataclass(frozen=True)
class Filter:
    key: str
    value: str
    comparative: str = field(default=Comparative.EQUAL)

    def compiled(self):
        comp_str = '' if self.comparative == Comparative.EQUAL else self.comparative + ':'
        return {self.key: comp_str + self.value}


@dataclass(frozen=True)
class Sort:
    value: str
    direction: str = field(default=SortDirection.ASCENDING)

    def compiled(self):
        return {'sort': self.value + ':' + self.direction}

@dataclass(frozen=True)
class Limit:
    value: int
    
    def compiled(self):
        return {'limit': self.value}