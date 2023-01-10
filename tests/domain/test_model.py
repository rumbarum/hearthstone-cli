import pytest

from stone.bootstrap import bootstrap
from stone.domain import command, event
from stone.domain.model import BattleField, Minion, Player


@pytest.fixture
def minions():
    minions = [Minion(attack=1, life=100) for _ in range(2)]
    return minions


@pytest.fixture
def players(minions):
    player1 = Player()
    player2 = Player()
    player1.minion_field.append(minions[0])
    player2.minion_field.append(minions[1])
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


def test_minion_melee_attack_player_with_damage_1_decrease_1_life(
    battle_field, message_bus
):
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    melee_attack = command.MeleeAttack(
        source=min1.uuid, target=pl2.uuid, attack=min1.attack
    )
    message_bus.handle(melee_attack)
    pl2.life = 29
    min1.life = 100
