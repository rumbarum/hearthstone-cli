from dataclasses import dataclass, field

import pytest

from stone.bootstrap import bootstrap
from stone.domain import commands, events, model
from stone.domain.model import BattleField, Card, Minion, Player


@dataclass
class Spell(model.Spell):
    name: str = "test_spell"
    attack: int = 6


@dataclass
class Minion(model.Minion):
    name: str = "test_minion"
    attack: int = 6
    life: int = 100


@dataclass
class SpellCard(model.Card):
    name: str = "test_spell_card"
    mana: int = 5
    object: model.CardObject = Spell


@dataclass
class MinionCard(model.Card):
    name: str = "test_minion_card"
    mana: int = 5
    object: model.CardObject = Minion


@pytest.fixture
def spell_card_with_mana_5():
    return SpellCard(mana=5)


@pytest.fixture
def minion_card_with_mana_5():
    return MinionCard(mana=5)


def test_player_succeed_initiate_card_with_enough_mana(
    battle_field, message_bus
):
    """
    given:
        1 player has 10 mana and
    when:
        handout card 5 mana minion card
    then:
        minion on field ,
    :return:
    """
    pl1, pl2 = battle_field.players.values()
    pl1.mana = 10
    minion_card = MinionCard(mana=5)
    minion_index = 3
    pl1.card_slot.append(minion_card)
    play_card_command = commands.PlayCard(
        player=pl1.uuid, card=minion_card.uuid, minion_field_index=minion_index
    )
    message_bus.handle(play_card_command)

    assert isinstance(pl1.minion_field[minion_index], MinionCard.object)
