from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Generator, Type, Union
from uuid import uuid4

import rich

from stone.domain import commands, events, model


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


CardObject = Union[Type[Spell] | Type[Minion]]


@dataclass(kw_only=True)
class Card:
    mana: int
    object: CardObject
    uuid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)


class Console:
    @classmethod
    def display_attakced(
        cls,
        source_name: str,
        source_uuid: str,
        target_name: str,
        target_uuid: str,
        attack: int,
    ) -> None:
        rich.print(
            f"""[green]{source_name}{source_uuid[:5]}[/green] damaged [green]{target_name}{target_uuid[:5]}[/green] by [red]{attack:3}[/red]"""
        )

    @classmethod
    def display_spell_used(
        cls,
        source_name: str,
        source_uuid: str,
        spell_name: str,
        spell_uuid: str,
        target_name: str,
        target_uuid: str,
        attack: int,
    ) -> None:
        rich.print(
            f"""[green]{source_name}{source_uuid[:5]}[/green]'s spell [yellow]{spell_name}{spell_uuid[:5]}[/yellow] damaged [green]{target_name}{target_uuid[:5]}[/green] by [red]{attack:3}[/red]"""
        )

    @classmethod
    def handle_card_played(
        cls, player_name: str, card_name: str, card_uuid: str
    ) -> None:
        rich.print(f"{player_name} play a {card_name}{card_uuid[:3]}")


@dataclass(kw_only=True)
class Player:
    name: str
    card_slot: list[Card] = field(default_factory=list)
    minion_field: list[Minion | None] = field(
        default_factory=lambda: list([None] * 7)
    )
    uuid: str = field(default_factory=lambda: str(uuid4()))
    life: int = 30
    mana: int = 0
    attack: int = 0
    spell_processing: list[Spell] = field(default_factory=list)
    spell_processed: list[Spell] = field(default_factory=list)

    def get_card_from_player(self, card_uuid: str) -> Card:
        for card in self.card_slot:
            if card_uuid == card.uuid:
                return card
        raise ValueError("NO_MATCHING_CARD")

    def get_spell_processing_from_player(self, spell_uuid: str) -> Spell:
        for idx, spell in enumerate(self.spell_processing):
            if spell.uuid == spell_uuid:
                return spell
        raise ValueError("NO_SPELL")

    def change_processing_to_process(self, spell_uuid: str) -> None:
        for idx, spell in enumerate(self.spell_processing):
            if spell.uuid == spell_uuid:
                self.spell_processed.append(self.spell_processing.pop(idx))
        raise ValueError("NO_SPELL")


@dataclass
class BattleField:
    players: dict[str, Player]
    message_slot: deque = field(default_factory=deque)
    console = Console

    def get_player_by_uuid(self, uuid: str) -> Player:
        player = self.players.get(uuid)
        if player is None:
            raise ValueError("NO_UUID")
        return player

    def get_minion_by_uuid(self, uuid: str) -> Minion:
        for player in self.players.values():
            for minion in player.minion_field:
                if minion is not None and minion.uuid == uuid:
                    return minion
        raise ValueError("NO_UUID")

    def _is_minion_exist(self, uuid: str) -> bool:
        for player in self.players.values():
            for minion in player.minion_field:
                if minion is not None and minion.uuid == uuid:
                    return True
        return False

    def _is_player_exist(self, uuid: str) -> bool:
        for k in self.players.keys():
            if uuid == k:
                return True
        return False

    def get_target_by_uuid(self, uuid: str) -> Player | Minion:
        if self._is_player_exist(uuid):
            return self.get_player_by_uuid(uuid)
        elif self._is_minion_exist(uuid):
            return self.get_minion_by_uuid(uuid)
        else:
            raise ValueError("NO_UUID")

    def collect_new_messages(self) -> Generator:
        while slot := self.message_slot:
            yield slot.popleft()

    def get_card_from_player(self, player_uuid: str, card_uuid: str):
        player = self.get_player_by_uuid(player_uuid)
        card = player.get_card_from_player(card_uuid)
        return card

    def melee_attack(self, source: str, target: str, attack: int) -> None:
        target_instance = self.get_target_by_uuid(target)
        source_instance = self.get_target_by_uuid(source)
        target_instance.life -= attack
        source_instance.life -= target_instance.attack
        self.message_slot.append(
            events.Attacked(source=source, target=target, attack=attack)
        )
        if target_instance.attack > 0:
            self.message_slot.append(
                events.Attacked(
                    source=target,
                    target=source,
                    attack=target_instance.attack,
                )
            )

    def ranged_attack(self, source: str, target: str, attack: int) -> None:
        target_instance = self.get_target_by_uuid(target)
        target_instance.life -= attack
        self.message_slot.append(
            events.Attacked(
                source=source,
                target=target,
                attack=attack,
            )
        )

    def use_spell(
        self,
        source: str,
        target: str,
        spell: str,
        attack: int,
    ) -> None:
        target_instance = self.get_target_by_uuid(target)
        target_instance.life -= attack
        self.message_slot.append(
            events.SpellUsed(
                source=source,
                target=target,
                attack=attack,
                spell=spell,
            )
        )

    def play_card(
        self, player: str, card: str, minion_field_index: int
    ) -> None:
        player_instance = self.get_player_by_uuid(player)
        card_instance = self.get_card_from_player(player, card)

        if player_instance.mana < card_instance.mana:
            rich.print("NOT ENOUGH MANA")
            return
        if (
            minion_field_index is not None
            and player_instance.minion_field[minion_field_index] is not None
        ):
            rich.print("ALREADY TAKEN POSITION")
            return
        if issubclass(card_instance.object, model.Minion):
            minion = card_instance.object()
            if minion_field_index is not None:
                player_instance.minion_field[minion_field_index] = minion
                rich.print(
                    f"{player_instance.uuid} play a card {card_instance.name} on {minion_field_index}"
                )
                self.message_slot.append(
                    events.CardPlayed(
                        player=player,
                        card=card,
                        minion_field_index=minion_field_index,
                    )
                )
