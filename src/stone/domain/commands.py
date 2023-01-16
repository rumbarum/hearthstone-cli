from dataclasses import dataclass


class Command:
    pass


@dataclass
class Attack(Command):
    target: str
    source: str


@dataclass
class MeleeAttack(Attack):
    attack: int


@dataclass
class RangedAttack(Attack):
    attack: int
