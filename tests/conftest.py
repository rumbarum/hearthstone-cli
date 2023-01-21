from dataclasses import dataclass, field

import pytest

from stone.bootstrap import bootstrap
from stone.domain import commands, events, model
from stone.domain.model import BattleField, Minion, Player


@dataclass
class MinionTest(model.Minion):
    name: str = "test_minion"
    attack: int = 1
    life: int = 100


@pytest.fixture
def minions():
    minions = [
        # Minion(attack=1, life=100, name="test_min", mana=1) for _ in range(2)
        MinionTest(),
        MinionTest(),
    ]
    return minions


@pytest.fixture
def players(minions):
    player1 = Player(name="test_pl1")
    player2 = Player(name="test_pl2")
    player1.minion_field[0] = minions[0]
    player2.minion_field[0] = minions[1]
    return player1, player2


@pytest.fixture
def battle_field(players) -> BattleField:
    player_dict = {player.uuid: player for player in players}
    field = BattleField(players=player_dict)
    return field


@pytest.fixture
def message_bus(battle_field):
    message_bus = bootstrap(battle_field)
    return message_bus


@pytest.fixture
def spell_with_attack_3():
    return model.Spell(attack=3, name="test_spell")
