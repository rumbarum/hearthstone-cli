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


@dataclass
class CardPlayed(Event):
    player: str
    card: str
    minion_field_index: int | None = None
    target: str | None = None
