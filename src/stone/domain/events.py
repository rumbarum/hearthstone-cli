from dataclasses import dataclass


class Event:
    pass


@dataclass
class Attacked:
    source: str
    target: str
    attack: int
