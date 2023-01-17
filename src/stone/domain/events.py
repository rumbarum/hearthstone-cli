from dataclasses import dataclass


class Event:
    pass


@dataclass
class Attacked(Event):
    source: str
    target: str
    attack: int


@dataclass
class SpellUsed(Event):
    source: str
    target: str
    spell: str
    attack: int
