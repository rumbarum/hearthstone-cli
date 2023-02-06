from dataclasses import dataclass, field

import pytest

from stone.bootstrap import bootstrap
from stone.domain import commands, events, model
from stone.domain.model import BattleField, Card, Minion, Player


@dataclass
class SampleSpell(model.Spell):
    name: str = "test_spell"
    attack: int = 6


@dataclass
class SampleMinion(model.Minion):
    name: str = "test_minion"
    attack: int = 6
    life: int = 100


@dataclass
class SpellCard(model.Card):
    name: str = "test_spell_card"
    mana: int = 5
    object: model.CardObject = SampleSpell


@dataclass
class MinionCard(model.Card):
    name: str = "test_minion_card"
    mana: int = 5
    object: model.CardObject = SampleMinion


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
        player 1 has 10 mana and
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
    pl1.hand.append(minion_card)
    play_card_command = commands.PlayCard(
        player=pl1.uuid,
        card=minion_card.uuid,
        minion_field_index=minion_index,
        target=None,
    )
    message_bus.handle(play_card_command)

    assert isinstance(pl1.minion_field[minion_index], MinionCard.object)


def test_player_draw_card_twice(battle_field, message_bus):
    """
    given:
        player 1 has 2 cards on dispenser
    when:
        draw a card twice
    then:
        cards on player 1's hand
    :return:
    """
    pl1, pl2 = battle_field.players.values()
    minion_card = MinionCard()
    spell_card = SpellCard()

    pl1.card_dispenser.append(minion_card)
    pl1.card_dispenser.append(spell_card)

    draw_card_command = commands.DrawCard(player=pl1.uuid)
    message_bus.handle(draw_card_command)
    message_bus.handle(draw_card_command)

    assert pl1.hand.pop(0) == minion_card
    assert pl1.hand.pop(0) == spell_card
