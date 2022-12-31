from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Player:
    card_slot: list = field(default_factory=list)
    uuid: str = field(default_factory=lambda: str(uuid4))
    life: int = 30
    mana: int = 0


@dataclass
class BattleField:
    message_slot: deque = field(default_factory=deque)
    players: list[Player] = field(default_factory=list)

    def get_player_by_uuid(self, uuid: str):
        for player in self.players:
            if uuid == player.uuid:
                return player

        raise ValueError("WRONG_UUID")
