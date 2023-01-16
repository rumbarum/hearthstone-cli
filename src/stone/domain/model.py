from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Generator
from uuid import uuid4

import rich

from stone.domain import commands, events


@dataclass
class Minion:
    attack: int
    life: int
    uuid: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Player:
    card_slot: list = field(default_factory=list)
    minion_field: list[Minion] = field(default_factory=list)
    uuid: str = field(default_factory=lambda: str(uuid4()))
    life: int = 30
    mana: int = 0
    attack: int = 0


@dataclass
class BattleField:
    players: dict[str, Player]
    message_slot: deque = field(default_factory=deque)

    def get_player_by_uuid(self, uuid: str) -> Player:
        player = self.players.get(uuid)
        if player is None:
            raise ValueError("WRONG_UUID")
        return player

    def get_minion_by_uuid(self, uuid: str) -> Minion:
        for player in self.players.values():
            for minion in player.minion_field:
                if minion.uuid == uuid:
                    return minion
        raise ValueError("NO_UUID")

    def get_target_by_uuid(self, uuid: str) -> Player | Minion:
        player = self.players.get(uuid)
        if player is not None:
            return player

        target_min = None
        for player in self.players.values():
            for minion in player.minion_field:
                if minion.uuid == uuid:
                    target_min = minion
        if target_min:
            return target_min
        else:
            raise ValueError("NO_UUID")

    def collect_new_messages(self) -> Generator:
        while slot := self.message_slot:
            yield slot.popleft()
