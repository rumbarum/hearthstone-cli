import pytest

from stone.bootstrap import bootstrap
from stone.domain import commands, events
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
    melee_attack = commands.MeleeAttack(
        source=min1.uuid, target=pl2.uuid, attack=min1.attack
    )
    message_bus.handle(melee_attack)
    assert pl2.life == 29
    assert min1.life == 100


def test_player_ranged_attack_minon_with_damage_50_decrease_50_life(
    battle_field, message_bus
):
    """
    given
        2 player with 1 minion each
    when
        pl2 attack pl1's minion
    then
        minion1 life decrease
        player1 life stay
    """
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    ranged_attack = commands.RangedAttack(
        source=pl2.uuid, target=min1.uuid, attack=50
    )
    message_bus.handle(ranged_attack)
    assert min1.life == 50
    assert pl2.life == 30


def test_display_console_minion_attack_other_minion(
    battle_field, message_bus, capsys
):
    """
    given
        2 player with 1 minion each
    when
        pl1 minion attack pl2 minion
    then
        display 2 message will show up
    """
    pl1, pl2 = battle_field.players.values()
    min1 = pl1.minion_field[0]
    min2 = pl2.minion_field[0]
    melee_attack = commands.MeleeAttack(
        source=min1.uuid, target=min2.uuid, attack=min1.attack
    )
    message_bus.handle(melee_attack)
    captured = capsys.readouterr()
    assert (
        f"""{min1.uuid[:5]} damaged {min2.uuid[:5]} by {min1.attack:3}\n{min2.uuid[:5]} damaged {min1.uuid[:5]} by {min2.attack:3}\n"""
        == captured.out
    )
