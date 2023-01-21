from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Generator, Union
from uuid import uuid4

import rich

from stone.domain import commands, events


@dataclass(kw_only=True)
class Spell:
    name: str
    attack: int
    uuid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)


@dataclass(kw_only=True)
class Minion:
    name: str
    attack: int
    life: int
    uuid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)


CardObject = Union[Spell | Minion]


@dataclass(kw_only=True)
class Card:
    mana: int
    object: CardObject
    uuid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)


@dataclass(kw_only=True)
class Player:
    name: str
    card_slot: list[Card] = field(default_factory=list)
    minion_field: list[Minion] = field(
        default_factory=lambda: list([None] * 7)
    )
    uuid: str = field(default_factory=lambda: str(uuid4()))
    life: int = 30
    mana: int = 0
    attack: int = 0

    def get_card_from_player(self, card_uuid: str):
        for card in self.card_slot:
            if card_uuid == card.uuid:
                return card
        raise ValueError("NO_MATCHING_CARD")


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
                if minion is not None and minion.uuid == uuid:
                    target_min = minion
        if target_min:
            return target_min
        else:
            raise ValueError("NO_UUID")

    def collect_new_messages(self) -> Generator:
        while slot := self.message_slot:
            yield slot.popleft()

    def get_card_from_player(self, player_uuid: str, card_uuid: str):
        player = self.get_player_by_uuid(player_uuid)
        card = player.get_card_from_player(card_uuid)
        return card
