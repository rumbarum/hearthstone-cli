from dataclasses import dataclass

from .model import Player


class Command:
    pass


@dataclass
class Attack(Command):
    attack: int
    target: str
    source: str
