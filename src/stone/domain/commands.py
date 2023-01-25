from dataclasses import dataclass, field


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


@dataclass
class UseSpell(Attack):
    spell: str


@dataclass
class PlayCard(Command):
    player: str
    card: str
    minion_field_index: int | None = None
    target: str | None = None


@dataclass
class DrawCard(Command):
    player: str
