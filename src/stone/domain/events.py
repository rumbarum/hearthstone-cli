from dataclasses import dataclass


class Event:
    pass


@dataclass
class Attacked(Event):
    source: str
    target: str
    attack: int
